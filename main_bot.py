# Code heavily inspired by:
# 'Introduction to Monte Carlo Tree Search'
# 07 September 2015, Jeff Bradberry
# http://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
#
# Adapter for Connect-4 by Maxime Cannoodt & Felix Guo

import numpy as np
import datetime
from random import choice
from math import log, sqrt

def current_player(board_history):
    '''
    Input: history of board (list of np.array)
    Assumes: len(states) > 0
    Method: bleh
    Output: player number (int) of whose turn it is
    '''
    current_state = board_history[-1]
    turns_by_1 = np.count_nonzero(current_state == 1)
    turns_by_2 = np.count_nonzero(current_state == 2)
    if turns_by_1 > turns_by_2:
        return 2
    if turns_by_2 > turns_by_1:
        return 1
    # case if turns_by_1 == turns_by_2
    previous_state = board_history[-2]
    turns_by_1 = np.count_nonzero(previous_state == 1)
    turns_by_2 = np.count_nonzero(previous_state == 2)
    if turns_by_1 > turns_by_2:
        return 1
    if turns_by_2 > turns_by_1:
        return 2


def next_state(board_history, move):
    '''
    Input: board (np.array), player (int) whose turn it is, move (int) column
    Assumes: move is an element of legal_moves(board)
    Method: in move column, find largest index with 0 and replace with player number
    Output: next_board (np.array) with updated move
    '''
    next_board = np.copy(board_history[-1])
    player = current_player(board_history)
    # print(next_board)

    try:
        next_board[np.where(next_board[:,move] == 0)[0][-1], move] = player
    except:
        print('!!!!! ERROR !!!!!')
        print(next_board)
        raise

    return next_board


def legal_moves(board):
    # Takes a sequence of game states representing the full
    # game history, and returns the full list of moves that
    # are legal plays for the current player.
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0].tolist()


def state_to_str(board):
    board = board.astype(int)
    board = board.astype(str)
    board = board.flatten().tolist()
    return ''.join(board)


def str_to_state(str):
    if len(str) == 6 * 7:
        out = np.array([c for c in str])
        return out.reshape((6, 7)).astype(float)


def scan_board(board):
    # Generator for all 4-in-a-row states (inspired by https://gist.github.com/poke/6934842)
    '''
    Input: board (np.array)
    Assumes: board.shape[0] > 3 and board.shape[1] > 3
    Method: creates a set for all 4-in-a-row shapes on the board.
    '''
    rows, cols  = board.shape
    horizontals = [board[row, col_start:col_start+4] for row in range(rows) for col_start in range(0, cols-3)]
    verticals = [board[row_start:row_start+4, col] for col in range(cols) for row_start in range(0, rows-3)]
    up_diags = [np.array([board[start_row-i, start_col+i] for i in range(4)]) for start_row in range(3, rows) for start_col in range(cols-3)]
    down_diags = [np.array([board[start_row+i, start_col+i] for i in range(4)]) for start_row in range(3) for start_col in range(cols-3)]
    return horizontals + verticals + up_diags + down_diags


def find_winner(board):
    '''
    Input: board (np.array)
    Output:
        0 if no winner,
        1 if player 1 wins,
        2 if player 2 wins,
        -1 if tie. (full board)
    '''
    for test in scan_board(board):
        if len(np.where(test)[0]) == 4:
            # if a winner is found
            if np.all(test == test[0]):
                return test[0]
    # if the game was tied
    if 0 not in board:
        return -1
    else:
        return 0


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board_history = kwargs.get('board_history', list())
        self.calculation_time = datetime.timedelta(seconds=kwargs.get('time', 0.5))
        self.max_moves = kwargs.get('max_moves', 100)
        self.C = kwargs.get('C', 1.4)

        self.wins = kwargs.get('wins', dict())
        self.plays = kwargs.get('plays', dict())


    def update(self, board):
        # Takes a game state, and appends it to the history.
        self.board_history.append(board)


    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.board_history[-1]
        player = current_player(state)
        legal = legal_moves(state)

        # If there's no legal moves, don't bother
        if not legal:
            return
        # if there's only one choice anyways
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        # Runs simulations as long as is allowed by hyperparameter 'time'
        # this should be less than 1.0 sec to conform to competition rules.
        while datetime.datetime.utcnow() - begin <self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(move, state_to_str(next_state(self.board_history, move))) for move in legal]

        # Print the number of simulations ran and time elapsed
        print(games, datetime.datetime.utcnow() - begin)

        # pick the move with the highest percentage of wins
        win_rate, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each legal move possible
        for x in sorted(
                ((100 * self.wins.get((player, S), 0) /
                      self.plays.get((player, S), 1),
                  self.wins.get((player, S), 0),
                  self.plays.get((player, S), 0), p)
                 for p, S in moves_states),
                reverse=True
        ):
            print('Column {3}: {0:.2f}% ({1} / {2})'.format(*x))

        print('Max depth searched:', self.max_depth)

        return move


    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins

        visited_states = set()
        history_copy = self.board_history[:]
        player = current_player(history_copy[-1])

        expand = True
        for i in range(self.max_moves):
            legal = legal_moves(history_copy[-1])
            move_states = [(p, state_to_str(next_state(history_copy, p))) for p in legal]

            if all(plays.get((player, S)) for p, S in move_states):
                # If there are statistics on all of the legal moves, use them.
                # applies the UCB1 formula: xi +- sqrt( 2 ln(n) / ni ) with:
                # xi = mean payout for move i
                # ni = #plays on move i
                # n  = #plays in total
                log_total = log(sum(plays[(player, S)] for p, S in move_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in move_states
                )
            else:
                # If there are no stats on this move, make an arbitrary decision
                move, state = choice(move_states)

            history_copy.append(str_to_state(state))

            # add dictionary entries for newly found game state
            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0
                if i > self.max_depth:
                    self.max_depth = i

            visited_states.add((player, state))

            player = current_player(str_to_state(state))
            winner = find_winner(str_to_state(state))
            if winner:
                break

        for (player, state) in visited_states:
            if (player, state) not in self.plays:
                continue # move along, nothing to see here

            # update occurrence value for given game state
            self.plays[(player, state)] += 1
            # if game state led to a win for this player,
            # update win value for given game state
            if player == winner:
                self.wins[(player, state)] += 1


def generate_move(board, player, saved_state=None):
    # HYPERPARAMETERS
    # time = amount of time allowed to run simulations.
    # max_moves = amount of moves ahead allowed in one simulation
    time = 0.9
    max_moves = 200


    # if board is empty (all 0), return center column
    if np.all(board == 0):
        AI = MonteCarlo(board, time=time, max_moves=max_moves)
        AI.update(board)
        board[5, 3] = player
        AI.update(board)
        return 3, (AI.board_history, AI.plays, AI.wins)

    # After the first move, start running the MonteCarlo class
    board_history, plays, wins = list(), dict(), dict()
    if saved_state:
        board_history, plays, wins = saved_state
    AI = MonteCarlo(board, time=time, max_moves=max_moves,
                    board_history=board_history, wins=wins, plays=plays)
    AI.update(board)
    move = AI.get_play()
    AI.update(next_state(AI.board_history, move))
    return move, (AI.board_history, AI.plays, AI.wins)

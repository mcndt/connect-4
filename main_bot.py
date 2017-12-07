# Code heavily inspired by:
# 'Introduction to Monte Carlo Tree Search'
# 07 September 2015, Jeff Bradberry
# http://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
#
# Adapter for Connect-4 by Maxime Cannoodt & Felix Guo

import numpy as np
import datetime
from random import choice


def current_player(board): # to-do: other method, this relies on a false assumption
    '''
    Input: board (np.array)
    Method: if even number of moves so far, return (player) 1
    Output: player number (int) of whose turn it is
    '''
    if len(np.where(board)[0])%2: return 1
    else: return 2


def next_state(board, player, move):
    '''
    Input: board (np.array), player (int) whose turn it is, move (int) column
    Assumes: move is an element of legal_moves(board)
    Method: in move column, find largest index with 0 and replace with player number
    Output: next_board (np.array) with updated move
    '''
    next_board = np.copy(board)
    next_board[np.where(next_board[:,move] == 0)[0][-1], move] = player
    return next_board


def legal_moves(board):
    # Takes a sequence of game states representing the full
    # game history, and returns the full list of moves that
    # are legal plays for the current player.
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]


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


def winner(board):
    '''
    Input: board (np.array)
    Method:
    Output: 0 if no winner, 1 if player 1 wins, 2 if player 2 wins
    '''
    for test in scan_board(board):
        if len(np.where(test)[0]) == 4:
            if np.all(test == test[0])
                return test[0]
    else:
        return 0


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        self.board = board
        self.states = list()
        self.calculation_time = datetime.timedelta(seconds=kwargs.get('time', 30))
        self.max_moves = kwargs.get('max_moves', 100)


    def update(self, state):
        # Takes a game state, and appends it to the history.


    def get_play(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin <self.calculation_time:
            # Runs simulations as long as is allowed by hyperparameter 'time'
            # this should be less than 1.0 sec to conform to competition rules.
            self.run_simulation()


    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        states_copy = self.states[:]
        state = states_copy[-1]

        for i in range(self.max_moves):
            # in the article, it says legal_moves(states_copy)
            legal = legal_moves(state)
            move = choice(legal)
            state = next_state(board, player, move)
            states_copy.append(state)

            winner = winner(state)
            if winner:
                break

            # to-do: make the function know who's playing for the next state













def generate_move(board, player, saved_state):
    if sum(board) == 0: # if board is empty (all 0), return center column
        return 3

    return choice(legal_moves(board))

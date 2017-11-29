import numpy as np
import random
import datetime

def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]

def current_player(board):
    '''
    Input: board (np.array)
    Method: if even number of moves so far, return (player) 1
    Output: player number (int) of whose turn it is
    '''
    if len(np.where(board)[0])%2: return 1
    else: return 2

def next_state(board,player,move):
    '''
    Input: board (np.array), player (int) whose turn it is, move (int) column
    Assumes: move is an element of legal_moves(board)
    Method: in move column, find largest index with 0 and replace with player number
    Output: next_board (np.array) with updated move
    '''
    next_board = np.copy(board)
    next_board[np.where(next_board[:,move] == 0)[0][-1],move] = player
    return next_board

# Generators for 4-in-a-row are taken from https://gist.github.com/poke/6934842
def horizontals(board):
    '''
    Input: board (np.array)
    Assumes: board.shape[1] > 3
    Method: creates a generator for all horizontal 4-in-a-row
    '''
    rows,cols = board.shape
    return [board[row,col_start:col_start+4] for row in range(rows) for col_start in range(0,cols-3)]

def verticals(board):
    '''
    Input: board (np.array)
    Assumes: board.shape[0] > 3
    Method: creates a generator for all vertical 4-in-a-row
    '''
    rows,cols = board.shape
    return [board[row_start:row_start+4,col] for col in range(cols) for row_start in range(0,rows-3)]

def up_diagonals(board):
    '''
    Input: board (np.array)
    Assumes: board.shape[0] > 3 and board.shape[1] > 3
    Method: creates a generator for all up-diagonal 4-in-a-row
    '''
    rows,cols = board.shape
    return [np.array([board[start_row-i,start_col+i] for i in range(4)]) for start_row in range(3,rows) for start_col in range(cols-3)]

def down_diagonals(board):
    '''
    Input: board (np.array)
    Assumes: board.shape[0] > 3 and board.shape[1] > 3
    Method: creates a generator for all down-diagonal 4-in-a-row
    '''
    rows,cols = board.shape
    return [np.array([board[start_row+i,start_col+i] for i in range(4)]) for start_row in range(3) for start_col in range(cols-3)]

def winner(board):
    '''
    Input: board (np.array)
    Method:
    Output: 0 if no winner, 1 if player 1 wins, 2 if player 2 wins
    '''
    for test in up_diagonals(board)+down_diagonals(board)+horizontals(board)+verticals(board):
        if len(np.where(test)[0]) == 4:
            if test[0] == test[1] and test[0] == test[2] and test[0] == test[3]:
                return test[0]
    else:
        return 0

# class MonteCarlo(object):
#     def __init__(self, board, **kwargs):
#         self.board = board
#         self.states = []
#         self.calculation_time = datetime.timedelta(seconds = kwargs.get('time', 1)) # 1sec is default
#         self.max_moves = kwargs.get('max_moves', 100) #Not sure what this does
#
#     def update(self, state):
#         self.states.append(state)
#
#     def get_move(self):
#         begin = datetime.datetime.utcnow()
#         while datetime.datetime.utcnow() - begin < self.calculation_time:
#             self.run_simulation()
#
#     def run_simulation(self):
#         states_copy = self.states[:]
#         state = states_copy[-1]
#
#     for t in range(self.max_moves):
#             legal = self.board.legal_plays(states_copy)
#
#             play = choice(legal)
#             state = self.board.next_state(state, play)
#             states_copy.append(state)
#
#             winner = self.board.winner(states_copy)
#             if winner:
#                 break

def generate_move(board, player, saved_state):
    if sum(board) == 0: # if board is empty (all 0), return center column
        return 3

    return legal_moves(board)[random.randint(0, len(legal_moves(board))-1)]

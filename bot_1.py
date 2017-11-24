import numpy as np
import random

def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]

def three_in_a_row(board): # Check for any three-in-a-rows and updates
    '''
    Input: np.array object representing board
    Output: int of column to either win the game or stop opponent from winning

    '''
    # Code to look for three-in-a-row
    # If three-in-a-row is player's, return winning move(s) if possible
    # If three-in-a-row is opponent's, return defending move(s) if needed
    pass

def generate_move(board, player, saved_state):
    return 4 if sum(board) == 0: # if board is empty (all 0), return center column


    return three_in_a_row(board) if three_in_a_row(board) # look for winning or defending move

    return legal_moves(board)[random.randint(0, len(legal_moves(board))-1)]

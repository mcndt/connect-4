import numpy as np
import random

def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]

def generate_move(board, player, saved_state):
    return legal_moves(board)[random.randint(0, len(legal_moves(board))-1)]
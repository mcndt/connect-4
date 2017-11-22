import numpy as np
import random

def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]

def generate_move(board, player, saved_state):
    return legal_moves(board)[random.randint(0, len(legal_moves(board))-1)]

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))

y = np.load('dump9.npy')
print(y)

p1 = np.where(y == 1, True, False)
p2 = np.where(y == 2, True, False)

B = np.zeros((6, 7, 2))
B[:, :, 0] = p1
B[:, :, 1] = p2

print(B[:, :, 0])
print(B[:, :, 1])

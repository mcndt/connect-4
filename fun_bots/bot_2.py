import numpy as np
from random import randint

def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]

def chain(board):
    '''
    Helper function for identifying vertical chains.
     Input: board
    output: list of one tuple per column, containing the player
    and chain length of the top chain per column.
    '''
    out = []
    for j in range(7):
        # for every column
        column, player, chain = j, None, None
        for i in range(5, -1, -1):
            # work every column from bottom to top
            if board[i, j] == 0:
                pass
            elif board[i, j] == player:
                chain += 1
            else:
                player = board[i, j]
                chain = 1
        out.append((column, player, chain))
    return out

def strat_column(board, player):
    '''
     Input: the current game board.
    Return: all columns eligible for victory by the bot.
    '''
    space = 6 - np.sum(np.where(board == 2, 1, board), axis=0)
    combos = [(j, p, c) for j, p, c in chain(board) if p == player]

    out = []
    for j, p, c in combos:
        if 4 - c <= space[j]:
            out.append(j)
    return tuple(out)

def generate_move(board, player, chosen_column=None):
    '''
    This bot will attempt to win by playing in one (randomly chosen) single column.
    When the column becomes unavailable for a future victory (less than 3 in a row),
    a new eligible column will be chosen. When no columns are eligible for this
    strategy, the bot falls back to the random selection of bot_1.
    '''
    if chosen_column == None:
        # first move by bot: choose random column
        chosen_column = legal_moves(board)[randint(0, len(legal_moves(board))-1)]
    elif chosen_column not in strat_column(board, player):
        # chosen column no longer eligible for victory: choose new column
        if len(strat_column(board, player)) > 0:
            # if there are still columns available for victory
            chosen_column = strat_column(board, player)[randint(0, len(strat_column(board, player))-1)]
        else:
            # if there are no eligible columns, play a random column.
            chosen_column = legal_moves(board)[randint(0, len(legal_moves(board))-1)]
    # if chosen column still eligible for victory: keep chosen column.

    # return twice, once for move and once for saved_state callback.
    return chosen_column, chosen_column

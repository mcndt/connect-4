import numpy as np


def legal_moves(board):
    return np.arange(board.shape[1])[np.sum(board == 0, axis=0) > 0]


def generate_move(board, player, saved_state):
    """Contains all code required to generate a move,
    given a current game state (board & player)

    Args:

        board (2D np.array):    game board (element is 0, 1 or 2)
        player (int):           your player number (token to place: 1 or 2)
        saved_state (object):   returned value from previous call

    Returns:

        action (int):                   number in [0, 6]
        saved_state (optional, object): will be returned to you the
                                        next time your function is called

    """
    return int(legal_moves(board)[0])

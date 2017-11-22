import numpy as np
import time

class ConnectFourException(Exception):
    pass


class ConnectFour(object):
    ROWS = 6
    COLS = 7


    def __init__(self):
        """Initialize an empty grid."""
        self.board = np.zeros((self.ROWS, self.COLS))
        self.players = [1.0, 2.0]
        self.longest_chain = {'length': 0, 'player': 0}

    def move(self, action, player):
        """Add a token to the grid.

        Args:
            action (int): The column where the token should be added.
            player (int): An index, specifying the player.

        Returns:
            board (np.array): A 2D-array, representing the grid.
            info (dict): A dictionary containing state information:
                            - whether the game is done or not
                            - the current points for both players
        """

        # Make sure the action is valid
        if action < 0 or action > self.COLS:
            raise ConnectFourException(
                'Action must be an integer between 0 and {}, was {}.'
                .format(self.COLS, action))

        digit = self.players[player]
        row = self.board[:, action]

        # If a player tries to add a token to a full column,
        # the token is discarded
        [spaces] = np.where(row == 0)
        if len(spaces) == 0:
            raise ConnectFourException(
                'Impossible to add a token to a full column.')

        pos = np.max(spaces)
        row[pos] = digit

        # Update the chain length
        chain_length = self._longest_chain((pos, action))
        if chain_length > self.longest_chain['length']:
            self.longest_chain = {'length': chain_length, 'player': player}

        return self.board, self._get_info()

    def _get_info(self):
        """Return state information.

        The game is done when:
            - their are no empty spaces left
            - a player connects 4 tokens

        Returns:
            info (dict): State information.
        """
        done = False

        if len(self.board[self.board == 0]) == 0:
            done = True

        if self.longest_chain['length'] >= 4:
            done = True

        points = [0, 0]
        for i, player in enumerate(self.players):
            if int(player) == int(self.longest_chain['player']) + 1:
                points[i] = 5 if self.longest_chain['length'] >= 4 else 1
            else:
                points[i] = -5 if self.longest_chain['length'] >= 4 else -1

        info = {
            'done': done,
            'points': points
        }

        return info

    def _get_digit(self, pos):
        """Fetch the digit (representing a player) for a position."""
        digit = self.board[pos]
        return digit

    def _update_pos(self, current_pos, move):
        """Add one to a position, based on the direction of the move.

        Args:
            current_pos (tuple): A tuple representing (y, x).
            move (tuple): A tuple representing (dy, dx).
        """
        new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
        return new_pos

    def _valid_pos(self, current_pos):
        """Check if a position is within the grid."""
        y, x = current_pos
        valid = (0 <= y < self.ROWS) and (0 <= x < self.COLS)
        return valid

    def _longest_chain_for_move(self, start_pos, move):
        """Calculate the chain a player can make for a single type of move,
        given a starting point, not counting the starting point.

        Args:
            start_pos (tuple)
            move (tuple)

        Returns:
            current_chain (int): The chain length.
        """
        current_chain = 0
        current_pos = self._update_pos(start_pos, move)

        while (self._valid_pos(current_pos) and
               self._get_digit(current_pos) == self._get_digit(start_pos)):
            current_chain += 1
            current_pos = self._update_pos(current_pos, move)

        return current_chain

    def _longest_chain_for_direction(self, start_pos, direction):
        """Calculate the chain a player can make for a single direction,
        given a starting point.

        Args:
            start_pos (tuple)
            direction (list): A list containing one or more `move` tuples.

        Returns:
            chain_length (int): The chain length.
        """
        chain_length = 1 + np.sum([
            self._longest_chain_for_move(start_pos, move)
            for move in direction])

        return chain_length

    def _longest_chain(self, start_pos):
        """Calculate the longest chain a player can make,
        given a starting point."""
        directions = [
            [(1, 0)],            # Vertical
            [(0, -1), (0, 1)],   # Horizontal
            [(-1, -1), (1, 1)],  # First diagonal
            [(1, -1), (-1, 1)]   # Second diagonal
        ]

        res = np.max([
            self._longest_chain_for_direction(start_pos, direction)
            for direction in directions])

        return res


def print_score(winning_player, points_player1, points_player2):
    print(
            'Game is over! Winner: {} || ' 'Current score: Challenger ' '{} -- {} Opponent'.format(winning_player,
                                                                                                   points_player1, points_player2)
    )



def play_connect_four(challenger_mover, opponent_mover, nb_games=5):
    """Play a game, consisting of `nb_games` rounds between two bots.

    Args:
        challenger_mover (function): an implemented generate_move function.
        opponent_mover (function): an implemented generate_move function.
        nb_games (int): the number of rounds to simulate
    """
    starting_player = np.random.randint(2)
    total_points = [0, 0]
    for game_number in range(nb_games):
        print('\n\n\nGame number: ', game_number+1)

        # Initialize new game
        connect_four = ConnectFour()
        challenger_saved_state, opponent_saved_state = None, None

        player = starting_player
        info = connect_four._get_info()

        # While the game is not done, keep making moves
        while not info['done']:
            # Get the move generator and saved state of current player
            generator, saved_state = [
                (challenger_mover, challenger_saved_state),
                (opponent_mover, opponent_saved_state)
            ][player]  # Player is equal to 0 or 1

            # Generate a move with the current player his generator and time it
            start = time.time()
            result = generator(connect_four.board, player+1, saved_state)
            move_time = time.time() - start

            # Generator can either return tuple or int
            if isinstance(result, tuple):
                action, saved_state = result
                if player:
                    opponent_saved_state = saved_state
                else:
                    challenger_saved_state = saved_state
            else:
                action = result

            # Print the updated state
            print('Player {} moved ({:f} seconds)...'.format(
                player + 1, np.around(move_time, 5)))
            try:
                connect_four.board, info = connect_four.move(action, player)
            # If an exception occurs, the other player wins the game
            except ConnectFourException as e:
                print('Illegal move made...', e)
                winning_player = (player + 1) % 2  # The other player wins
                total_points[winning_player] += 5
                print_score(winning_player + 1, total_points[0],
                            total_points[1])
                info = None
                break
            print(connect_four.board)
            print('-'*33)

            # Switch player for next turn
            player = (player + 1) % 2

        # Points will contain a positive and negative number after the game
        # The index with the positive value corresponds to the winning player.
        if info is not None:
            winning_player = np.argmax(info['points'])
            total_points[winning_player] += info['points'][winning_player]
            print_score(winning_player + 1, total_points[0], total_points[1])

        # Switch starting player for the next round
        starting_player = (starting_player + 1) % 2


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
#        IMPORT YOUR OWN BOT PLAYERS BELOW          #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

from bot_1 import generate_move as random_mover
from query_bot import generate_move as query_mover

# Include two generate_move functions below
play_connect_four(random_mover, query_mover)

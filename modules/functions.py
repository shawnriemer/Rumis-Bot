import pandas as pd
import numpy as np
import random
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO


class Competitor:
    def __init__(self, owner, number, color):
        self.owner = owner
        self.number = number
        self.color = color
        self.still_playing = True
        self.piece_list = [
            self.number * np.array([[[1, 1, 1, 1]]]),
            self.number * np.array([[[1, 1, 1]]]),
            self.number * np.array([[[1, 1]]]),
            self.number * np.array([[[1, 0, 0], [1, 1, 1]]]),
            self.number * np.array([[[1, 1], [1, 1]]]),
            self.number * np.array([[[1, 0], [1, 1]]]),
            self.number * np.array([[[0, 1, 0], [1, 1, 1]]]),
            self.number * np.array([[[0, 1, 1], [1, 1, 0]]]),
            self.number * np.array([[[1, 0], [1, 1]], [[0, 0], [1, 0]]]),
            self.number * np.array([[[1, 0], [1, 1]], [[0, 0], [0, 1]]]),
            self.number * np.array([[[0, 1], [1, 1]], [[0, 0], [1, 0]]])
        ]
        self.piece_names_list = [
            '4x1', '3x1', '2x1', 'L', 'square', 'corner', 'pipe', 'bend', 'archer', 'twistL', 'twistR'
        ]
        self.piece_profile_positions = (0, 0, 0, 0, 0, 0)
        self.turn = 0

    def draw_pieces(self, grid, players, x=0, y=0, z=0, k1=0, k2=0, k3=0):
        for piece, piece_name in zip(self.piece_list, self.piece_names_list):
            empty_grid = Board(grid.board_name)
            piece = np.rot90(np.rot90(np.rot90(piece, k=k1, axes=(0, 1)), k=k2, axes=(1, 2)), k=k3, axes=(0, 2))
            # If a voxel can't be made then give up on that piece
            try:
                layer = fill_out(piece, empty_grid.grid, x, y, z)
                # Perform legality checks
                if ((grid.grid * layer).max() != 0) or ((grid.grid * layer).min() != 0):
                    pass
                    # print('piece in the way')
                    # raise ValueError
                if self.turn > 1:
                    adjacent, adjacent_bool = check_adjacent(grid.grid, layer, self.number)
                    if adjacent_bool is False:
                        pass
                        # print('adjacent_bool = False')
                        # raise ValueError
                supported_bool = check_supported(grid.grid, layer, self.number)
                if supported_bool is False:
                    pass
                    # print('supported_bool = False')
                    # raise ValueError

                # Replace overlapping pieces with 5
                piece_grid_add = grid.grid + layer
                piece_grid_mult = grid.grid * layer
                piece_grid = np.where(piece_grid_mult != 0, 5, piece_grid_add)

                # Match up to how it's graphed
                layer = np.rot90(np.rot90(layer, k=1, axes=(0, 2)), k=3, axes=(0, 1))
                piece_grid = np.rot90(np.rot90(piece_grid, k=1, axes=(0, 2)), k=3, axes=(0, 1))

                # Create color DataFrame
                color_rgb_map = {
                    'red': [1, 0, 0],
                    'yellow': [1, 1, 0],
                    'green': [0, 1, 0],
                    'blue': [0, 0, 1],
                    'cyan': [0, 1, 1],
                    'magenta': [1, 0, 1]
                }

                piece_grid = np.where(piece_grid == -1, 0, piece_grid)

                color = []
                for i, level in enumerate(piece_grid):
                    for j, row in enumerate(level):
                        for k, val in enumerate(row):
                            if layer[i, j, k] > 0:
                                opacity = 1
                            else:
                                opacity = 0.25
                            if val == 0:
                                color.append('none')
                            elif val == 1:
                                color.append(color_rgb_map[players['1'].color] + [opacity])
                            elif val == 2:
                                color.append(color_rgb_map[players['2'].color] + [opacity])
                            elif val == 3:
                                color.append(color_rgb_map[players['3'].color] + [opacity])
                            elif val == 4:
                                color.append(color_rgb_map[players['4'].color] + [opacity])
                            elif val == 5:
                                color.append([0, 0, 0])
                df = pd.DataFrame({'color': color})

                # Create graph and save image
                ax = plt.figure(figsize=(3.2, 2.4)).add_subplot(projection='3d')
                ax.voxels(piece_grid, facecolors=np.array(df.color).reshape(piece_grid.shape), edgecolor='k')
                ax.set_box_aspect(grid.aspect_ratio)
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                ax.set_zticklabels([])
                ax.figure.savefig(f'static//{piece_name}.png', format='png')
                plt.clf()
                plt.close()
            # Catch when a piece has moved off the board
            except ValueError:
                source_path = 'static//invalid_move.png'
                destination_path = f'static//{piece_name}.png'
                shutil.copy(source_path, destination_path)

        full_piece_names_list = [
            '4x1', '3x1', '2x1', 'L', 'square', 'corner', 'pipe', 'bend', 'archer', 'twistL', 'twistR'
        ]
        for piece_name in list(set(full_piece_names_list) - set(self.piece_names_list)):
            source_path = 'static//invalid_move.png'
            destination_path = f'static//{piece_name}.png'
            shutil.copy(source_path, destination_path)


class Board:
    def __init__(self, board):
        if board.lower() == 'chullpa':
            self.board_name = 'chullpa'
            self.grid = np.zeros((8, 4, 5))
            self.aspect_ratio = [1, 1, 1.55]
        elif board.lower() == 'pirka':
            self.board_name = 'pirka'
            self.grid = np.zeros((4, 8, 6))
            self.grid[:, 3:, :3] = -1
            self.aspect_ratio = [1, 1.7, 0.7]
        elif board.lower() == 'coricancha':
            self.board_name = 'coricancha'
            self.grid = np.zeros((4, 8, 8))
            self.grid[1:, 0, :] = -1
            self.grid[1:, 7, :] = -1
            self.grid[1:, :, 0] = -1
            self.grid[1:, :, 7] = -1
            self.grid[2:, 1, 1:7] = -1
            self.grid[2:, 6, 1:7] = -1
            self.grid[2:, 1:7, 1] = -1
            self.grid[2:, 1:7, 6] = -1
            self.grid[3:, 2, 2:6] = -1
            self.grid[3:, 5, 2:6] = -1
            self.grid[3:, 2:6, 2] = -1
            self.grid[3:, 2:6, 5] = -1
            self.aspect_ratio = [1, 1.3, 0.5]
        elif board.lower() == 'pisac':
            self.board_name = 'pisac'
            self.grid = np.zeros((8, 8, 8))
            self.grid[:, 0:6, 0] = -1
            self.grid[:, 0:6, 7] = -1
            self.grid[:, 0:4, 1] = -1
            self.grid[:, 0:4, 6] = -1
            self.grid[:, 0:2, 2] = -1
            self.grid[:, 0:2, 5] = -1
            self.grid[1:, 7, :] = -1
            self.grid[2:, 6, :] = -1
            self.grid[3:, 5, :] = -1
            self.grid[4:, 4, :] = -1
            self.grid[5:, 3, :] = -1
            self.grid[6:, 2, :] = -1
            self.grid[7:, 1, :] = -1
            self.aspect_ratio = [1, 1.3, 1]
        elif board.lower() == 'cucho':
            self.board_name = 'cucho'
            self.grid = np.zeros((5, 8, 8))
            self.grid[:, 0:4, 0:4] = -1
            self.grid[1:, 0, 4:] = -1
            self.grid[2:, 1, 4:] = -1
            self.grid[3:, 2, 4:] = -1
            self.grid[4:, 3, 4:] = -1
            self.grid[1:, 4:, 0] = -1
            self.grid[2:, 4:, 1] = -1
            self.grid[3:, 4:, 2] = -1
            self.grid[4:, 4:, 3] = -1
            self.aspect_ratio = [1, 1.35, 0.7]
        elif board.lower() == 'tambo':
            self.board_name = 'tambo'
            self.grid = np.zeros((4, 7, 7))
            self.grid[:, :2, 5:] = -1
            self.grid[:, 5:, :2] = -1
            self.grid[:, 2, 2] = -1
            self.aspect_ratio = [1, 1.35, 0.55]

    def draw_board(self, title_string, players, rotation=3):
        # Rotate grid for graphing software, replace illegal positions with 0 to avoid errors
        grid_t = np.rot90(np.rot90(self.grid, k=1, axes=(0, 2)), k=rotation, axes=(0, 1))
        grid_t = np.where(grid_t == -1, 0, grid_t)

        # Loop through each square to record it's color for the graph
        color = []
        for i, layer in enumerate(grid_t):
            for j, row in enumerate(layer):
                for k, val in enumerate(row):
                    if val == 0:
                        color.append('none')
                    elif val == 1:
                        color.append(players['1'].color)
                    elif val == 2:
                        color.append(players['2'].color)
                    elif val == 3:
                        color.append(players['3'].color)
                    elif val == 4:
                        color.append(players['4'].color)
        df = pd.DataFrame({'color': color})

        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(grid_t, facecolors=np.array(df.color).reshape(grid_t.shape), edgecolor='k')

        ax.set_box_aspect(self.aspect_ratio)

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

        ax.set_title(title_string)

        # TODO: activate this
        # ax.figure.savefig(f'static//board_{270 - (90 * rotation)}.png', format='png')

        return ax

    def get_results(self):
        grid = self.grid
        grid = np.where(grid == -1, 0, grid)
        missing = np.ones((grid.shape[1], grid.shape[2]))
        count_dict = {}
        for team in np.unique(grid):
            count_dict[team] = 0

        for i in range(1, grid.shape[0] + 1):
            # Grab layer, only keep spots with no higher piece, count points
            layer = grid[i * -1, :, :]
            layer = layer * missing
            unique, counts = np.unique(layer, return_counts=True)
            layer_count_dict = dict(zip(unique, counts))
            # Add to team's point totals
            for team in layer_count_dict.keys():
                count_dict[team] = count_dict[team] + layer_count_dict[team]
            layer_missing = np.where(grid[i * -1, :, :] == 0, 1, 0)
            missing = missing * layer_missing

        # Put together result string
        count_dict.pop(-1, None)
        count_dict.pop(0, None)
        winner = int(max(count_dict, key=count_dict.get))
        result_str = f'Player {winner} Wins!!!\n'
        for player in count_dict.keys():
            result_str += f'\nPlayer {int(player)}: {count_dict[player]}'
        return result_str


def check_adjacent(grid, layer, player, turn_2=False):
    """Return a boolean indicating if the selected move meets the adjacent rule."""
    # Grab the board's dimensions and create a blank board
    n_layers, n_rows, n_columns = grid.shape
    adjacent = np.zeros((n_layers, n_rows, n_columns))

    # Loop through each square on board
    for i, level in enumerate(grid):
        for j, row in enumerate(level):
            for k, val in enumerate(row):

                # True if the spot belongs to the current player, unless it's round 1
                player_check = (val > 0) if turn_2 is True else (val == player)

                # Create a DataFrame of every open spot adjacent to any of the current player's pieces
                if player_check:
                    # Spots above current spots
                    if (i < (n_layers - 1)) and (grid[i + 1, j, k] == 0):
                        adjacent[i + 1, j, k] = player

                    # Spots above/below current spots
                    if (j > 0) and (grid[i, j - 1, k] == 0):
                        adjacent[i, j - 1, k] = player
                    if (j < (n_rows - 1)) and (grid[i, j + 1, k] == 0):
                        adjacent[i, j + 1, k] = player

                    # Spots left/right of current spots
                    if (k > 0) and (grid[i, j, k - 1] == 0):
                        adjacent[i, j, k - 1] = player
                    if (k < (n_columns - 1)) and (grid[i, j, k + 1] == 0):
                        adjacent[i, j, k + 1] = player

    # Make sure the selected piece includes at least one spot adjacent to the player's existing pieces
    adjacent_bool = False if (adjacent * layer).max() == 0 else True

    return adjacent, adjacent_bool


def check_supported(grid, layer, player):
    """Return a boolean indicating if the selected move meets the overhanging rule."""
    # Create the board if the selected move is played
    new_grid = grid + layer

    # Loop through each square on board
    for i, level in enumerate(new_grid):
        for j, row in enumerate(level):
            for k, val in enumerate(row):
                if val == player:
                    # Spots below can't be empty
                    if (i > 0) and (new_grid[i - 1, j, k] == 0):
                        return False
    return True


def play_move(player, grid, start, turn_2):
    """Randomly make a move for the computer.

    Parameters
    ----------
    player : Competitor
        The current player's Competitor object.
    grid : Board
        The current game's board.
    start : bool
        Indicates if this is the first turn.
    turn_2 : bool
        Indicates if this is the first round  # TODO: is this round or turn 2?

    Returns
    -------
    Board
        Updated Board object
    string
        The name of the piece being played, if a valid move was found
    """
    # TODO: this function sucks
    attempt_counter = 0

    while True:
        # Randomly choose a piece
        piece_i = random.randint(0, len(player.piece_list) - 1)
        piece = player.piece_list[piece_i]

        # Randomly rotate piece and place its location
        oriented_piece = orient(piece)
        layer = fill_out(oriented_piece, grid.grid)

        # Check if it is a legal move

        # Are any spots already taken/void?
        if ((grid.grid * layer).max() == 0) and ((grid.grid * layer).min() == 0):
            spot_bool = True
        else:
            spot_bool = False

        # Check if adjacent to opponent piece (second piece only)
        if turn_2 is True:
            adjacent, adjacent_bool = check_adjacent(grid.grid, layer, player.number, turn_2=True)
        # Check if adjacent to an existing piece (unless it's the first turn)
        elif (spot_bool is True) and (start is False):
            adjacent, adjacent_bool = check_adjacent(grid.grid, layer, player.number)
        # The first piece doesn't have a rule
        else:
            adjacent_bool = True
            adjacent = ''

        # Check that the piece is not hanging
        if (spot_bool is True) and (adjacent_bool is True):
            supported_bool = check_supported(grid.grid, layer, player.number)
        else:
            supported_bool = False

        # Make that play if it is legal
        if (spot_bool is True) and (adjacent_bool is True) and (supported_bool is True):
            grid.grid += layer
            del player.piece_list[piece_i]
            piece_name = player.piece_names_list.pop(piece_i)

            return grid, piece_name

        # Keep track of attempts
        attempt_counter += 1
        if attempt_counter == 5000:
            player.still_playing = False
            return grid, None


def human_move(player_turn, players, grid, piece_i):
    """Play the human's move.

    Parameters
    ----------
    player_turn : string
        The current player.
    players : dictionary
        Dictionary of Competitor objects.
    grid : Board
        The current game's Board.
    piece_i : string
        The name of the piece being played.

    Returns
    -------
    dictionary
        Updated dictionary of Competitor objects
    Board
        Updated Board object
    """
    # Grab the current player's object
    print(f'Human move for player {player_turn}')
    player = players[player_turn]

    # Remove selected piece from available list
    piece_i = player.piece_names_list.index(piece_i)
    piece = player.piece_list.pop(piece_i)
    piece_name = player.piece_names_list.pop(piece_i)

    # Orient the piece as chosen and make the move
    x, y, z, rot_x, rot_y, rot_z = player.piece_profile_positions
    piece = orient(piece, rot_x, rot_y, rot_z)
    layer = fill_out(piece, grid.grid, x, y, z)
    grid.grid += layer

    # Create the figure for each orientation of the board
    title_string = f'Player {player_turn} Turn {player.turn}: {piece_name}'
    create_figures(title_string, players, grid)
    plt.close('all')

    return players, grid


def orient(piece, k1=None, k2=None, k3=None):
    """Returns the (randomly) rotated piece."""
    # Randomly orient the piece if no orientation is given
    if k1 is None:
        k1 = random.randint(0, 3)
    if k2 is None:
        k2 = random.randint(0, 3)
    if k3 is None:
        k3 = random.randint(0, 3)

    return np.rot90(np.rot90(np.rot90(piece, k=k1, axes=(0, 1)), k=k2, axes=(1, 2)), k=k3, axes=(0, 2))


def fill_out(piece, grid, row_start=None, col_start=None, stack_start=None):
    """Returns the (randomly) translated piece."""
    # Grab the dimensions of the piece and board
    n_layers, n_rows, n_columns = grid.shape
    stacks, rows, cols = piece.shape

    # Calculate the limits of where the piece can be played
    stack_max_start = n_layers - stacks
    row_max_start = n_rows - rows
    col_max_start = n_columns - cols

    # Randomly place the piece if no position is given
    if stack_start is None:
        stack_start = random.randint(0, stack_max_start)
    if row_start is None:
        row_start = random.randint(0, row_max_start)
    if col_start is None:
        col_start = random.randint(0, col_max_start)

    # Calculate the left/right padding needed for each axis
    stack_top_pad = stack_start
    stack_bottom_pad = stack_max_start - stack_start
    row_top_pad = row_start
    row_bottom_pad = row_max_start - row_start
    col_left_pad = col_start
    col_right_pad = col_max_start - col_start

    return np.pad(piece,
                  ((stack_top_pad, stack_bottom_pad), (row_top_pad, row_bottom_pad), (col_left_pad, col_right_pad)))


def start_game(
    board_name,
    check1, check2, check3, check4,
    cphuman1, cphuman2, cphuman3, cphuman4,
    color1, color2, color3, color4
):
    """Start the game."""
    # Create each player object, store in a dict
    p1 = Competitor(cphuman1, 1, color1)
    players = {'1': p1}
    if check2:
        p2 = Competitor(cphuman2, 2, color2)
        players['2'] = p2
    if check3:
        p3 = Competitor(cphuman3, 3, color3)
        players['3'] = p3
    if check4:
        p4 = Competitor(cphuman4, 4, color4)
        players['4'] = p4

    # Create grid object
    grid = Board(board_name)

    # Draw first human's pieces
    try:
        if p1.owner == 'human':
            p1.draw_pieces(grid, players)
        elif p2.owner == 'human':
            p2.draw_pieces(grid, players)
        elif p3.owner == 'human':
            p3.draw_pieces(grid, players)
        elif p4.owner == 'human':
            p4.draw_pieces(grid, players)
    except UnboundLocalError:
        p1.draw_pieces(grid, players)

    return players, grid


def play_turn(turn, players, grid):
    """Play a turn."""
    # Figure out whose turn it is and get their available pieces
    num_players = len(players)
    player_num = (turn % num_players) + 1
    player = players[str(player_num)]

    # Indicate if it's the player's first turn
    start = True if turn <= 1 else False

    # The first round has different rules, create an indicator
    turn_2 = True if (turn > 0) and (turn < num_players) else False

    # Randomly play a piece by trial and erroring the rules
    if (player.still_playing is True) and (len(player.piece_list) > 0):
        grid, piece_name = play_move(player, grid, start, turn_2)
        if piece_name is None:
            title_string = f'Player {player_num} Maxed Out Attempts'
            create_figures(title_string, players, grid)
        else:
            title_string = f'Player {player_num} Turn {turn + 1}: {piece_name}'
            create_figures(title_string, players, grid)
    if (player.still_playing is True) and (len(player.piece_list)) == 0:
        title_string = f'Player {player_num} Out of Pieces'
        create_figures(title_string, players, grid)
        player.still_playing = False

    plt.close('all')

    return players, grid


def create_figures(title_string, players, grid):
    """Create and save figures for each rotation of the board."""
    # Create figures
    ax = grid.draw_board(title_string, players=players)
    ax_90 = grid.draw_board(title_string, rotation=2, players=players)
    ax_180 = grid.draw_board(title_string, rotation=1, players=players)
    ax_270 = grid.draw_board(title_string, rotation=0, players=players)

    # Save figures
    ax.figure.savefig('static//board_0.png', format='png')
    ax_90.figure.savefig('static//board_90.png', format='png')
    ax_180.figure.savefig('static//board_180.png', format='png')
    ax_270.figure.savefig('static//board_270.png', format='png')

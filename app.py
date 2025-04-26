from flask import Flask, render_template, request, jsonify, session
from modules.functions import *
import jsonpickle

app = Flask(__name__)
app.secret_key = '234897f134951'  # Required to use session


@app.route('/', methods=['GET', 'POST'])
def hello():
    session.clear()
    session['turn'] = 0
    if request.method == "POST":
        # Retrieve attributes for each player and the board
        check1 = True if request.form.get("check1") == 'on' else False
        check2 = True if request.form.get("check2") == 'on' else False
        check3 = True if request.form.get("check3") == 'on' else False
        check4 = True if request.form.get("check4") == 'on' else False
        cphuman1 = request.form.get("cp_human1")
        cphuman2 = request.form.get("cp_human2")
        cphuman3 = request.form.get("cp_human3")
        cphuman4 = request.form.get("cp_human4")
        color1 = request.form.get("color1")
        color2 = request.form.get("color2")
        color3 = request.form.get("color3")
        color4 = request.form.get("color4")
        board_name = request.form.get("game_board")

        # Create player and grid objects
        players, grid = start_game(
            board_name,
            check1, check2, check3, check4,
            cphuman1, cphuman2, cphuman3, cphuman4,
            color1, color2, color3, color4
        )

        # TODO: Draw blank board

        # Save game's data
        session['players'] = jsonpickle.encode(players)
        session['grid'] = jsonpickle.encode(grid)

    return render_template('index.html')


@app.route('/nextturn', methods=['POST'])
def nextTurn():
    data = request.get_json()  # retrieve the data sent from JavaScript
    print(f"Turn: {session['turn']}")

    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])

    player_turn = str((session['turn'] % len(players)) + 1)
    next_player_turn = str(((session['turn'] + 1) % len(players)) + 1)
    print(f"Player {player_turn}'s turn, next turn: {next_player_turn} (# players: {len(players)})")

    if players[player_turn].owner == 'cp':
        players, grid = play_turn(session['turn'], players, grid)
    elif players[player_turn].owner == 'human':
        players, grid = human_move(player_turn, players, grid, data['piece'])

    # Reset profile places for each player
    for player in players.values():
        player.piece_profile_positions = (0, 0, 0, 0, 0, 0)

    players[player_turn].turn += 1
    players[next_player_turn].draw_pieces(grid, players)

    # Save game's data
    session['players'] = jsonpickle.encode(players)
    session['grid'] = jsonpickle.encode(grid)
    session['turn'] += 1

    return jsonify({'turn': session['turn'], 'piece_list': players[next_player_turn].piece_names_list})  # return the result to JavaScript


@app.route('/movePiece', methods=['POST'])
def move_piece():
    print('app.py move_piece()')
    data = request.get_json()
    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])
    player_turn = str((session['turn'] % len(players)) + 1)
    next_player_turn = str(((session['turn'] + 1) % len(players)) + 1)
    move = data['move']

    player = players[player_turn]
    current_x, current_y, current_z, rot_x, rot_y, rot_z = player.piece_profile_positions
    if move == 'right':
        player.piece_profile_positions = (current_x + 1, current_y, current_z, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x + 1, current_y, current_z, rot_x, rot_y, rot_z)
    elif move == 'left':
        player.piece_profile_positions = (current_x - 1, current_y, current_z, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x - 1, current_y, current_z, rot_x, rot_y, rot_z)
    elif move == 'away':
        player.piece_profile_positions = (current_x, current_y + 1, current_z, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y + 1, current_z, rot_x, rot_y, rot_z)
    elif move == 'towards':
        player.piece_profile_positions = (current_x, current_y - 1, current_z, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y - 1, current_z, rot_x, rot_y, rot_z)
    elif move == 'up':
        player.piece_profile_positions = (current_x, current_y, current_z + 1, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y, current_z + 1, rot_x, rot_y, rot_z)
    elif move == 'down':
        player.piece_profile_positions = (current_x, current_y, current_z - 1, rot_x, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y, current_z - 1, rot_x, rot_y, rot_z)
    elif move == 'x':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x, rot_y, rot_z + 1)
        players[player_turn].draw_pieces(grid, players, current_x, current_y, current_z, rot_x, rot_y, rot_z + 1)
    elif move == 'y':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x + 1, rot_y, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y, current_z, rot_x + 1, rot_y, rot_z)
    elif move == 'z':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x, rot_y + 1, rot_z)
        players[player_turn].draw_pieces(grid, players, current_x, current_y, current_z, rot_x, rot_y + 1, rot_z)

    session['players'] = jsonpickle.encode(players)

    return jsonify({'piece_list': players[next_player_turn].piece_names_list})  # return the result to JavaScript


@app.route('/reset', methods=['POST'])
def reset():
    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])
    player_turn = str((session['turn'] % len(players)) + 1)
    players[player_turn].piece_profile_positions = (0, 0, 0, 0, 0, 0)
    players[player_turn].draw_pieces(grid, players, 0, 0, 0, 0, 0, 0)
    session['players'] = jsonpickle.encode(players)
    return jsonify('abc')  # TODO: useless


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

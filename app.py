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
        board_name = request.form.get("none_n")
        players, grid = start_game(4, board_name)
        # players, grid, ax, ax_90, ax_180, ax_270 = play_turn(session['turn'], players, grid)
        players, grid = play_turn(session['turn'], players, grid)

        session['players'] = jsonpickle.encode(players)
        session['grid'] = jsonpickle.encode(grid)

        # ax.figure.savefig('static//test_0.png', format='png')
        # ax_90.figure.savefig('static//test_90.png', format='png')
        # ax_180.figure.savefig('static//test_180.png', format='png')
        # ax_270.figure.savefig('static//test_270.png', format='png')

    return render_template('index.html')


@app.route('/nextturn', methods=['POST'])
def nextTurn():
    data = request.get_json()  # retrieve the data sent from JavaScript
    print(data)

    session['turn'] += 1

    print(f"Turn: {session['turn']}")

    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])
    players[str(2)].draw_pieces(grid, 0, 0, 0, 0, 0, 0)  # TODO: hardcoded

    if (session['turn'] % 4) + 1 != 2:  # TODO: hardcoded
        # players, grid, ax, ax_90, ax_180, ax_270 = play_turn(session['turn'], players, grid)
        players, grid = play_turn(session['turn'], players, grid)
    else:
        # players, grid, ax, ax_90, ax_180, ax_270 = human_move(players, grid, data['piece'])
        players, grid = human_move(players, grid, data['piece'])

    # Reset profile places for each player
    for player in players.values():
        player.piece_profile_positions = (0, 0, 0, 0, 0, 0)

    session['players'] = jsonpickle.encode(players)
    session['grid'] = jsonpickle.encode(grid)

    # ax.figure.savefig('static//test_0.png', format='png')
    # ax_90.figure.savefig('static//test_90.png', format='png')
    # ax_180.figure.savefig('static//test_180.png', format='png')
    # ax_270.figure.savefig('static//test_270.png', format='png')

    return jsonify({'turn': session['turn']})  # return the result to JavaScript


@app.route('/movePiece', methods=['POST'])
def move_piece():
    print('app.py move_piece()')
    data = request.get_json()
    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])
    move = data['move']

    player = players[str(2)]  # TODO: hardcoded
    current_x, current_y, current_z, rot_x, rot_y, rot_z = player.piece_profile_positions
    if move == 'right':
        player.piece_profile_positions = (current_x + 1, current_y, current_z, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x + 1, current_y, current_z, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'left':
        player.piece_profile_positions = (current_x - 1, current_y, current_z, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x - 1, current_y, current_z, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'away':
        player.piece_profile_positions = (current_x, current_y + 1, current_z, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y + 1, current_z, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'towards':
        player.piece_profile_positions = (current_x, current_y - 1, current_z, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y - 1, current_z, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'up':
        player.piece_profile_positions = (current_x, current_y, current_z + 1, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y, current_z + 1, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'down':
        player.piece_profile_positions = (current_x, current_y, current_z - 1, rot_x, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y, current_z - 1, rot_x, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'x':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x, rot_y, rot_z + 1)
        players[str(2)].draw_pieces(grid, current_x, current_y, current_z, rot_x, rot_y, rot_z + 1)  # TODO: hardcoded
    elif move == 'y':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x + 1, rot_y, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y, current_z, rot_x + 1, rot_y, rot_z)  # TODO: hardcoded
    elif move == 'z':
        player.piece_profile_positions = (current_x, current_y, current_z, rot_x, rot_y + 1, rot_z)
        players[str(2)].draw_pieces(grid, current_x, current_y, current_z, rot_x, rot_y + 1, rot_z)  # TODO: hardcoded

    session['players'] = jsonpickle.encode(players)

    return jsonify({'result': 'hi'})  # return the result to JavaScript


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

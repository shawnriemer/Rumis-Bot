from flask import Flask, render_template, request, jsonify, session
from modules.functions import *
# from flask_cors import CORS
import jsonpickle

app = Flask(__name__)
# CORS(app)
app.secret_key = '234897f134951'  # Required to use session


@app.route('/', methods=['GET', 'POST'])
def hello():
    session['turn'] = 0
    if request.method == "POST":
        board_name = request.form.get("none_n")
        players, grid = start_game(4, board_name)
        players, grid, ax = play_turn(session['turn'], players, grid)

        session['players'] = jsonpickle.encode(players)
        session['grid'] = jsonpickle.encode(grid)

        ax.figure.savefig('static//test.png', format='png')
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # retrieve the data sent from JavaScript
    # process the data using Python code
    result = data['value'] * 2
    return jsonify({'result': result})  # return the result to JavaScript


@app.route('/nextturn', methods=['POST'])
def nextTurn():
    data = request.get_json()  # retrieve the data sent from JavaScript
    # process the data using Python code
    session['turn'] += 1

    print(f"Turn: {session['turn']}")

    players = jsonpickle.decode(session['players'])
    grid = jsonpickle.decode(session['grid'])
    players, grid, ax = play_turn(session['turn'], players, grid)
    session['players'] = jsonpickle.encode(players)
    session['grid'] = jsonpickle.encode(grid)

    ax.figure.savefig('static//test.png', format='png')
    return jsonify({'turn': session['turn']})  # return the result to JavaScript


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

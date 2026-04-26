# app.py
# Flask server - handles API requests from the frontend
# Two endpoints: /move (human move) and /reset (new game)

import os
from flask import Flask, request, jsonify, render_template
from game import Board, HUMAN, AI, EMPTY
from ai import get_ai_move

# Template folder is one level up from api/ (at project root)
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reset", methods=["POST"])
def reset():
    # return a fresh empty board
    board = Board()
    return jsonify({
        "grid": board.grid,
        "status": "playing",
        "message": "Game started! Your turn."
    })


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    grid = data["grid"]
    col = data["col"]

    board = Board.from_grid(grid)

    # validate the move
    if not board.is_valid_move(col):
        return jsonify({"error": "Invalid move"}), 400

    # human drops piece
    board.drop_piece(col, HUMAN)

    # check if human won
    if board.check_win(HUMAN):
        return jsonify({
            "grid": board.grid,
            "status": "human_win",
            "message": "You win! 🎉"
        })

    # check draw after human move
    if board.is_full():
        return jsonify({
            "grid": board.grid,
            "status": "draw",
            "message": "It's a draw!"
        })

    # AI takes its turn
    ai_col = get_ai_move(board)
    board.drop_piece(ai_col, AI)

    # check if AI won
    if board.check_win(AI):
        return jsonify({
            "grid": board.grid,
            "status": "ai_win",
            "ai_col": ai_col,
            "message": "Computer wins! Better luck next time."
        })

    # check draw after AI move
    if board.is_full():
        return jsonify({
            "grid": board.grid,
            "status": "draw",
            "ai_col": ai_col,
            "message": "It's a draw!"
        })

    return jsonify({
        "grid": board.grid,
        "status": "playing",
        "ai_col": ai_col,
        "message": "Your turn!"
    })


if __name__ == "__main__":
    app.run(debug=True)

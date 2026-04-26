# ai.py
# Minimax with alpha-beta pruning - same algorithm, nothing changed

import math
from game import ROWS, COLS, EMPTY, HUMAN, AI

DEPTH = 5


def score_window(window, player):
    opponent = HUMAN if player == AI else AI
    score = 0

    my_count = window.count(player)
    empty_count = window.count(EMPTY)
    opp_count = window.count(opponent)

    if my_count == 4:
        score += 100
    elif my_count == 3 and empty_count == 1:
        score += 5
    elif my_count == 2 and empty_count == 2:
        score += 2

    if opp_count == 3 and empty_count == 1:
        score -= 4

    return score


def evaluate_board(board, player):
    total_score = 0

    # center column preference
    center_col = [board.grid[r][COLS // 2] for r in range(ROWS)]
    total_score += center_col.count(player) * 3

    # horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board.grid[row][col + i] for i in range(4)]
            total_score += score_window(window, player)

    # vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board.grid[row + i][col] for i in range(4)]
            total_score += score_window(window, player)

    # diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board.grid[row + i][col + i] for i in range(4)]
            total_score += score_window(window, player)

    # diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            window = [board.grid[row + i][col - i] for i in range(4)]
            total_score += score_window(window, player)

    return total_score


def minimax(board, depth, alpha, beta, is_maximizing):
    if board.is_terminal():
        if board.check_win(AI):
            return None, 999999
        elif board.check_win(HUMAN):
            return None, -999999
        else:
            return None, 0

    if depth == 0:
        return None, evaluate_board(board, AI)

    valid_cols = board.get_valid_columns()
    best_col = valid_cols[0]

    if is_maximizing:
        best_score = -math.inf
        for col in valid_cols:
            board.drop_piece(col, AI)
            _, score = minimax(board, depth - 1, alpha, beta, False)
            board.remove_piece(col)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return best_col, best_score
    else:
        best_score = math.inf
        for col in valid_cols:
            board.drop_piece(col, HUMAN)
            _, score = minimax(board, depth - 1, alpha, beta, True)
            board.remove_piece(col)
            if score < best_score:
                best_score = score
                best_col = col
            beta = min(beta, score)
            if alpha >= beta:
                break
        return best_col, best_score


def get_ai_move(board):
    col, _ = minimax(board, DEPTH, -math.inf, math.inf, True)
    return col

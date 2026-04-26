# game.py
# Same game logic as before, just adapted to work with Flask
# No printing here - the frontend handles displaying the board

ROWS = 6
COLS = 7

EMPTY = 0
HUMAN = 1
AI = 2


class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def is_valid_move(self, col):
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def get_valid_columns(self):
        return [c for c in range(COLS) if self.is_valid_move(c)]

    def drop_piece(self, col, player):
        for row in range(ROWS - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = player
                return row
        return -1

    def remove_piece(self, col):
        for row in range(ROWS):
            if self.grid[row][col] != EMPTY:
                self.grid[row][col] = EMPTY
                return

    def check_win(self, player):
        # horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    return True
        # vertical
        for row in range(ROWS - 3):
            for col in range(COLS):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    return True
        # diagonal down-right
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    return True
        # diagonal down-left
        for row in range(ROWS - 3):
            for col in range(3, COLS):
                if all(self.grid[row + i][col - i] == player for i in range(4)):
                    return True
        return False

    def is_full(self):
        return len(self.get_valid_columns()) == 0

    def is_terminal(self):
        return self.check_win(HUMAN) or self.check_win(AI) or self.is_full()

    def to_dict(self):
        # convert board to a simple dict so Flask can send it as JSON
        return {"grid": self.grid}

    @staticmethod
    def from_grid(grid):
        # rebuild a Board object from a grid (sent from frontend)
        b = Board()
        b.grid = grid
        return b

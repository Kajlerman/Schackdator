# Responsible for storing information about the current state of a chess game. It will also be responsible for determining the valid moves at the
# current state. It will also keep a move log.

class GameState():
    def __init__(self):
        # Board is an 8x8 2D list, each element of the list has 2 characters
        # The first character represents the color of the piece, 'b' och 'w'
        # The second character represents the type of piece, 'R', 'N', 'B', 'Q' or 'K'
        # "--" represents an empty space with no piece
        self.board = [ # Maybe change this one to numpy array to increase speed
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
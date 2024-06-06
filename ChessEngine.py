# Responsible for storing information about the current state of a chess game. It will also be responsible for determining the valid moves at the
# current state and keep a move log

class GameState():
    def __init__(self):
        # Board is an 8x8 2D list, each element of the list has 2 characters
        # The first character represents the color of the piece, "b" and "w"
        # The second character represents the type of piece, "R", "N", "B", "Q" or "K"
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
        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, 
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    # Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # Swap players
        if move.pieceMoved == "wK": # Update the king's position
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    # Undo the last move
    def undoMove(self):
        if len(self.moveLog) != 0: # Make sure there's a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Switch turns back
            if move.pieceMoved == "wK": # Update the king's position
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    # All moves considering checks
    def getValidMoves(self):
    # 1) Generate all possible moves
        moves = self.getAllPossibleMoves()

        # 2) Test each move for validity
        for i in range(len(moves)-1, -1, -1):  # Iterate backwards to safely remove elements
            move = moves[i]
            self.makeMove(move) # Make possible move
            self.whiteToMove = not self.whiteToMove  # Switch back to threatened king's turn

            # 3) Check if move leaves king in check
            if self.inCheck():
                moves.remove(move)  # Remove move if it leaves king in check
            self.undoMove()
            self.whiteToMove = not self.whiteToMove  # Switch turns back

#        print(f"Valid moves:", [move.getChessNotation() for move in moves])

        # Determine checkmate or stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    # Determine if the current player is in check
    def inCheck(self):
        kingPos = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        return self.squaredUnderAttack(kingPos[0], kingPos[1])


#    # Determine if the enemy can attack the square r, c
    def squaredUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # Switch to opponent's turn
        oppMoves = self.getAllPossibleMoves() # Generate all of opponent's possible moves
        self.whiteToMove = not self.whiteToMove  # Switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    # All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Number of rows
            for c in range(len(self.board[r])): # Number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # Calls the appropiate move function based on piece type
        return moves

    # Get all pawn moves for pawn located at row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # White pawn moves
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r-1 ,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # Captures to the left
                if self.board[r-1][c-1][0] == "b": # Enemy piece to capture
                    moves.append(Move((r, c), (r-1 ,c-1), self.board))
            if c+1 <= 7: # Captures to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1 ,c+1), self.board))

        else: # Black pawn moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1 ,c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1 ,c+1), self.board))

    # Get all rook moves for rook located at row, col and add these moves to the list
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8): # The rook can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # Friendly piece invalid
                        break
                else: # Off board invalid
                    break

    # Get all knight moves for knight located at row, col and add these moves to the list
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (2, -1), (2, 1), (1, -2), (1, 2)) # Knight moves
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # Not an allied piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # Get all bishop moves for bishop located at row, col and add these moves to the list
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1)) # Diagonally up-left, up-right, down-right, down-left
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    # Get all queen moves for queen located at row, col and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # Get all king moves for king located at row, col and add these moves to the list
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)) # King moves
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    # Maps keys to values
    # Key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    #Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # Change this later to real chess notation
        return Move.getRankFile(self.startRow, self.startCol) + Move.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(r, c):
        return Move.colsToFiles[c] + Move.rowsToRanks[r]
    

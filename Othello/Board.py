
# Imports
from tkinter import *
from Constants import *
from Piece import *
from copy import *

# Board Class 
class Board(object):
    BLACK_PIECES = 2
    WHITE_PIECES = 2
    TOTAL_PIECES = 4
    MAXIMUM_PIECES = ROWS * COLUMNS

    # Constructor - draws the board and keep tracks of values. 
    # Takes a root, width, height, rows, cols, and background for the board
    def __init__(self, root, width, height, rows, cols, background):
        self.board = []
        self.root = root
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.background = background
        self.canvas = Canvas(root, width = width, height = height, bg = background)

        # Creates the board during initialization
        self.createBoard()

    # drawSquares - draws the pattern for the board.
    def drawSquares(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.canvas.create_line(row, col * ROW_GAP, col * self.width, col * ROW_GAP, fill="black")
                self.canvas.create_line(row * COLUMN_GAP, col * self.height, row * COLUMN_GAP, row * self.height, fill = "black")
    
    # getPiece - gets a piece on the board based on row and col
    def getPiece(self, row, col):
        if(row < 0 or row >= 8 or col < 0 or col >= 8):
            return 1
        return self.board[row][col]
    
    # flipTiles - flip the tiles on the board from one color to the next
    def flipTiles(self, piece_to_place, valid_moves, color):
        # We get the values of the valid moves.
        # This is an array of moves that need to be flipped based on the move
        flip_tiles = valid_moves[piece_to_place]
        # for every value in flip_tiles, we will update the color of that piece and add to the respective color.
        for i in flip_tiles:
            row = i[0]
            col = i[1]
            self.getPiece(row,col).updateColor(color)
            if(color == BLACK):
                self.BLACK_PIECES += 1
                self.WHITE_PIECES -= 1
            else:
                self.WHITE_PIECES += 1
                self.BLACK_PIECES -= 1

    # undoMove - undoes a move.
    def undoMove(self, piece_to_place, valid_moves, color, original_black_score, original_white_score):
        tiles_were_flipped = valid_moves[piece_to_place]
        for i in tiles_were_flipped:
            row = i[0]
            col = i[1]
            self.getPiece(row,col).updateColor(color)
        self.BLACK_PIECES = original_black_score
        self.WHITE_PIECES = original_white_score
    
    # removePiece - removes a piece from the board
    def removePiece(self, row, col, original_total_piece):
        self.updateBoard(row, col, None)
        self.TOTAL_PIECES = original_total_piece
    
    # opponent - gets the opponent color
    def opponent(self, color):
        return BLACK if color == WHITE else WHITE

    # isValidMove - checks and see if the move would be a valid move
    def isValidMove(self, row, col):
        if(self.getPiece(row, col) == 0 and (row >= 0 and row < 8) and (col >= 0 and col < 8)):
            return True
        return False
    
    # drawValidMoveCircle - draws the valid move circle on the board.
    def drawValidMoveCircle(self, row, col):
        x_center = row * SQUARE_SIZE + SQUARE_SIZE // 2
        y_center = col * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - 40
        x0 = x_center - radius
        y0 = y_center - radius
        x1 = x_center + radius
        y1 = y_center + radius
        self.canvas.create_oval(y0, x0, y1, x1, fill = BLUE, tags=ASSIST)
    
    # calculateScore - calculates the value of a piece for the AI. It takes a color
    def calculateScore(self, color, square_weights):
        # set a total value to 0
        total = 0
        # We loop through the board and if we get a 0, we continue
        # Else if we find our piece, we add the weight of the square to the total
        # if its an opponenet we subtract the value of the square from the total
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.board[row][col] == 0):
                    continue
                if(self.board[row][col].getColor() == color):
                    total += square_weights[row][col]
                else:
                    total -= square_weights[row][col]
        # we return the total
        return total

    # getValidMoves - gets the valid moves of the color
    def getValidMoves(self, color):
        # we get the opponents color
        opp = self.opponent(color)
        # we set an empty dictionary for the valid moves
        valid_moves = {}
        # we loop through the board
        for row in range(self.rows):
            for col in range(self.cols):
                # get the current piece and the row and col
                current_piece = self.getPiece(row, col)
                # if the piece matches our color and the piece isnt a 0 or 1, meaning its empty or off the board
                if((current_piece != 0 and current_piece != 1) and current_piece.getColor() == color):
                    # we loook in all directions of our current Piece
                    for d in DIRECTIONS:
                        # We create an array of tiles to flip that will store the value
                        tilesToFlip = []
                        # We get the x and y value of the piece
                        x_start = current_piece.getRow()
                        y_start = current_piece.getCol()
                        # We add the x and y value to the direction and check if a piece is there
                        board_x = x_start + d[0]
                        board_y = y_start + d[1]
                        # we get the next piece based on the direction
                        next_piece = self.getPiece(board_x, board_y)
                        # if its 0, meaning its an empty space, we go to the next piece
                        if(next_piece == 0):
                            continue
                        # if it the opponets color and its not a 0 or one, its a tile to flip
                        while((next_piece != 0 and next_piece != 1) and next_piece.getColor() == opp):
                            # we append the value to the tilesToFlip array,
                            tilesToFlip.append((board_x, board_y))
                            # We then increment in this direction again until we reach 0 or 1
                            board_x += d[0]
                            board_y += d[1]
                            next_piece = self.getPiece(board_x,board_y)
                        # once we stop going through pieces, we check if this move is valid
                        # if it is, we append it to the valid moves dictionary
                        if(self.isValidMove(board_x, board_y)):
                            # we get a key based on the valid moves
                            key = (board_x, board_y)
                            check_key = valid_moves.get(key)
                            # we check if this key already exists in the dictionary, if it does, it appends the values to this key.
                            # else we create a new key-value and add it to the dictionary
                            if(check_key):
                                for i in range(len(tilesToFlip)):
                                    valid_moves[key].append(tilesToFlip[i])
                            else:
                                valid_moves.update({(board_x, board_y): tilesToFlip})
        # we return valid moves
        return valid_moves

    # addPiece - add a piece to the board based on row, col, and color
    def addPiece(self, row, col, color):
        self.updateBoard(row, col, color)
        if(color == BLACK):
            self.BLACK_PIECES += 1
        else:
            self.WHITE_PIECES += 1
        self.TOTAL_PIECES += 1

    # gameOver - we check if the game is over
    def gameOver(self):
        if(self.TOTAL_PIECES == self.MAXIMUM_PIECES):
            return True
        return False
    
    # createBoard - we define the initial board state
    def createBoard(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if(row == 3 and col == 3):
                    self.board[row].append(Piece(row, col, WHITE))
                elif(row == 3 and col == 4):
                    self.board[row].append(Piece(row, col, BLACK))
                elif(row == 4 and col == 3):
                    self.board[row].append(Piece(row, col, BLACK))
                elif(row == 4 and col == 4):
                    self.board[row].append(Piece(row, col, WHITE))
                else:
                    self.board[row].append(0)

    # updateBoard - we update the board based on a piece being agged
    def updateBoard(self, row, col, color):
        if(color == None):
            self.board[row][col] = 0
        else:
            self.board[row][col] = Piece(row, col, color)
    
    # drawBoard - we draw the board on the canvas
    def drawBoard(self):
        self.drawSquares()
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.board[row][col]
                if(piece != 0):
                    piece.draw(self.canvas)
    
    # packBoard - we pack the canvas.
    def packBoard(self):
        self.canvas.pack()
    
    # clearBoard - we clear the board based on the some value. By default its all.
    def clearBoard(self, value="all"):
        self.canvas.delete(value)
'''
    Amani Cheatham
    102-81-556
    Due: November 13, 2022
    Assignment #3
    This program will Implement Othello, also known as Reversi, game with two players and an AI
    using the Mini-Max algorithm as well as alpha-beta pruning.
    This is the AI class. This is where the minimax algorithm is and the alpha-beta pruning 
'''

# Imports
from tkinter import *
from Constants import *
from Board import *
from Piece import *
from Game import *
import copy

# AI CLASS
class AI(object):
    DEBUG = True
    # Defines the instance of the AI class. It takes a color this AI should be and defines the board as None
    # We need the board for the AI to play the game by itself and see all possible moves before selecting one.
    def __init__(self, color):
        self.board = None
        self.board_weights = [
                              [120,-20,20,5,5,20,-20,120],
                              [-20,-40,-5,-5,-5,-5,-40,-20],
                              [20,-5,15,3,3,15,-5,20],
                              [5,-5,3,3,3,3,-5,5],
                              [5,-5,3,3,3,3,-5,5],
                              [20,-5,15,3,3,15,-5,20],
                              [-20,-40,-5,-5,-5,-5,-40,-20],
                              [120,-20,20,5,5,20,-20,120],
                              ]
        self.color = color
        self.boardStates = 0

    # getColor: Returns the color of the AI
    def getColor(self):
        return self.color

    # setBoard: sets the board equal to the value. This is how "copy" the board.
    def setBoard(self, value):
        self.board = value
    
    # heuristic: This functions checks what moves are good for the ai and what moves are bad.
    def heuristic(self, legal_move_count):
        # If the game is over, we calculate to see which piece has more pieces.
        # If the opposite color has the most pieces, we return MINIMUM, cause we will LOSE in this case.
        # Else, we return MAXIMUM, as this is a state where we will win.
        sum1 = self.board.BLACK_PIECES - self.board.WHITE_PIECES
        sum2 = self.board.BLACK_PIECES + self.board.WHITE_PIECES
        if(self.board.gameOver()):
            if(self.color == BLACK): 
                if(self.board.WHITE_PIECES > self.board.BLACK_PIECES):
                    return MINIMUM
                else:
                    return MAXIMUM
            else:
                if(self.board.BLACK_PIECES > self.board.WHITE_PIECES):
                    return MINIMUM
                else:
                    return MAXIMUM

        # We do some math to calculate how good the move is
        return self.board.calculateScore(self.color, self.board_weights) + ((sum1) / (sum2)) + (legal_move_count * -(sum1/sum2))
    
    # getBoardStates - prints the number of board states it viewed.
    def getBoardStates(self):
        if(self.DEBUG):
            print("TOTAL NUMBER OF STATES: {}".format(self.boardStates))
        self.boardStates = 0
    # minimax - The algorithm that simulates the game and return the best possible move it can play.
    # valid_moves - the set of valid moves the piece can make. We only use it to check the length for the heuristic function
    # Piece - The piece we want to place. This will simulate the game if we place this piece
    # Depth - How far down the tree we want to go. This will tell how us far ahead the AI will check
    # Alpha - The maximum value of which each play is worth. Used for alpha beta pruning
    # Beta - The minimum value of which each play is worth. Used for alpha beta pruning.
    # MaximizingPlayer - A boolean that tells wether we are maximizing a player or minimizing player
    # Color - The color of the piece to use.
    # Total_pieces - The total pieces at this current state of the board. Helps keep track as we play the simulation
    # current_black_pieces - the total black pieces at this current state of the board. Helps keep track as we play the simulation.
    # current_white_pieces - the total white pieces at this current state of the board. Helps keep track as we play the simulation.
    def minimax(self, valid_moves, Piece, depth, alpha, beta, maxamizingPlayer, color, total_pieces, current_black_pieces, current_white_pieces):
        # gets the X and Y value from the Piece to play on the board
        x = Piece[0]
        y = Piece[1]
        # Calculates how many times this function is called per move.
        # We get the opponent colors
        opp = self.board.opponent(color)
        # We get the length of legal moves to use for calculations in heuristics functions
        legal_moves = len(valid_moves)
        # The base case. If we hit 0 in our depth or the game is over or we have no valid moves.
        if(depth == 0 or self.board.gameOver() or valid_moves == {}):
            # We undo the move we have placed
            self.board.undoMove(Piece, valid_moves, opp, current_black_pieces, current_white_pieces)
            # We remove the piece from the board
            self.board.removePiece(x,y, total_pieces)
            # We update the boardStates by 1
            self.boardStates += 1
            # We return the heuristic of the move aka the value of which we believe this move will cost high
            return self.heuristic(legal_moves)
        
        # The maxing part of Mini Maxing. We are trying to get the value of the will give us the highest value of the played piece
        if maxamizingPlayer:
            # We set max_value to MINIMUM, which is negative infinity.ss
            max_eval = MINIMUM
            # We add this piece to a mock board 
            self.board.addPiece(x,y,color)
            # We check what the board would look like after we play this move
            self.board.flipTiles(Piece,valid_moves, color)
            # We get the moves now from the opponenet after flipping them
            child_valid_moves = self.board.getValidMoves(opp)
            # We get the keys of the opponents move. 
            child_valid_moves_keys = child_valid_moves.keys()
            # For every key in child key, we're are going to call min max. The key is every possible move made from this move.
            for key in child_valid_moves_keys:
                # We create an evaluate that returns the value from the minimax recursive call. 
                evaluate = self.minimax(child_valid_moves, key, depth - 1, alpha, beta,False, opp, self.board.TOTAL_PIECES, self.board.BLACK_PIECES, self.board.WHITE_PIECES)
                # We get the max of the evaluation and the maxEval
                max_eval = max(max_eval, evaluate)
                # We set alpha equal to the maximum value of alpha and the current evaluation
                alpha = max(alpha, evaluate)
                if(beta <= alpha):
                    break
            # We undo the move
            self.board.undoMove(Piece, valid_moves, opp, current_black_pieces, current_white_pieces)
            # We remove the Piece from the board and update pieces
            self.board.removePiece(x,y,total_pieces)
            # We return the max eval
            return max_eval
        else:
            # We set min eval to MAXIMUM, which is positive infinity
            min_eval =  MAXIMUM
            # We add the piece to the board
            self.board.addPiece(x,y,color)
            # We flip the tiles to the color
            self.board.flipTiles(Piece,valid_moves, color)
            # We get the child moves after the Piece
            child_valid_moves = self.board.getValidMoves(opp)
            # We get the keys of chikd keys
            child_valid_moves_keys = child_valid_moves.keys()
            # For every key, aka points to play, we call minimax on that key.
            for key in child_valid_moves_keys:
                # We set evaluate to equal the value from minimax
                evaluate = self.minimax(child_valid_moves, key, depth - 1, alpha, beta, True, opp, self.board.TOTAL_PIECES, self.board.BLACK_PIECES, self.board.WHITE_PIECES)
                # We get the minimum from evaluate and mini eval
                min_eval = min(min_eval, evaluate)
                # We get the minimum from evaluate and the beta value
                beta = min(beta, evaluate)
                # We check if beta is less than alpha and if it is, we prune.
                if(beta <= alpha):
                    break
            # We undo the move
            self.board.undoMove(Piece, valid_moves, opp, current_black_pieces, current_white_pieces)
            # We remove the piece
            self.board.removePiece(x,y, total_pieces)
            # We return minimal val
            return min_eval



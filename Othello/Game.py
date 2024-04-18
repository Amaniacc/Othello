# Imports
from tkinter import *
from Constants import *
from Board import *
from Piece import *
from AI import AI

# Game Class
class Game(object):
    HELPER_PADDING = 40
    CURRENT_INDEX = 0
    KEYS_LIST = []
    DEBUG = False

    # Constructor - takes a root for the game, player 1 and player 2, defined as BLACK and WHITE respectively.
    def __init__(self, root, player1 = BLACK, player2 = WHITE):
        self.root = root
        self.player1 = player1
        self.player2 = player2
        self.whiteIsInvalid = False
        self.blackIsInvalid = False
        self._init()
    
    # update - how we will update the board
    def update(self):
        self.board.clearBoard()
        self.board.drawBoard()
    
    # def reset - resets the game entirely.
    def reset(self):
        self._init()

    # getSelectedColor - returns the color of the selectedPlayer.
    # If its an ai - we call the AI's getColor function
    def getSelectedColor(self):
        if(isinstance(self.selected_player, AI)):
            return self.selected_player.getColor()
        return self.selected_player
    
    # private init - this is what we call when we reset the game.
    def _init(self):
        self.selected_player = self.player1
        self.board = Board(self.root, WIDTH, HEIGHT, ROWS, COLUMNS, BACKGROUND)
        self.valid_moves = {}

    # change_turn - changes the turn of the current player to the other player
    def change_turn(self):
        if(self.selected_player == self.player1):
            self.selected_player = self.player2
        else:
            self.selected_player = self.player1
        # we reset valid moves, KEY_LIST, and CURRENT_INDEX
        self.resetValidMoves()
        self.KEYS_LIST = []
        self.CURRENT_INDEX = 0
    
    # debugAI - we debug the AI.
    def debugAI(self, list_of_moves):
        if(self.DEBUG):
            print(list_of_moves)
    
    # gameOver - returns if the game is over
    def gameOver(self):
        return self.board.gameOver()
    
    # resetValidMoves - resets the valid moves
    def resetValidMoves(self):
        self.valid_moves = {}
    
    # getCurrentIndex - returs the current Index
    def getCurrentIndex(self):
        return self.CURRENT_INDEX
    
    # updateCurrentIndex - updates current index
    def updateCurrentIndex(self, value):
        self.CURRENT_INDEX = value
        
    # findValidMoves - gets the possible moves from the current state of the board.
    def findValidMoves(self):
        self.valid_moves = self.board.getValidMoves(self.getSelectedColor())
        self.generateKeysList()
    
    # flipTiles - flip the tiles of the board
    def flipTiles(self, piece_to_play):
        self.board.flipTiles(piece_to_play, self.valid_moves, self.getSelectedColor())

    # resetInvalid - resets the invalid state so we dont quit the game by accident
    def resetInvalid(self):
        self.blackIsInvalid = False
        self.whiteIsInvalid = False
    
    # playTurn - plays the turn of the selectedPlayer
    def playTurn(self):
        # first, we find the valid moves of the current board with the color.
        self.findValidMoves()
        # we draw the valid moves on the canvas
        self.getValidMoves()
        # If valid moves is empty, we will swap turns and have the next player play their turn
        if(self.valid_moves == {}):
            # If we reach a state where either player cant play, we call game over.
            if(self.whiteIsInvalid == True and self.blackIsInvalid == True):
                self.gameOver()
            # Print when the the current player has no valid moves.
            print("{} has no valid moves: Swapping turns!!".format(self.getSelectedColor()))
            # We check and see which color didnt have valid moves and update the isValid of the respective color
            if(self.getSelectedColor() == BLACK):
                self.blackIsInvalid = True
            else:
                self.whiteIsInvalid = True
            # we change turns
            self.change_turn()
            # We play the next turn
            self.playTurn()
        # if the players is an AI - they play their moves
        if(isinstance(self.selected_player, AI)):
            # We create a temp AI values to hold the heuristic for each move, temp_key for the key in dictionary
            # and temp_value for the value of the heuristic
            temp_AI_values = {}
            temp_key = None
            temp_value = MINIMUM
            # We reorder the valid moves so the most flips will go through first. This makes our minimax algorithm more effective as we look at the good moves first
            reordered_valid_moves = dict(sorted(self.valid_moves.items(), key=lambda item: len(item[1]), reverse=True))
            # we set the AI's board to the current board state.
            self.selected_player.setBoard(self.board)
            # for every key in the valid moves, we need to find the value of it, so we call the minimax function on all the moves
            for key in reordered_valid_moves.keys():
                # we get the value of the moves of valid moves
                value = self.selected_player.minimax(reordered_valid_moves, key, DIFFICULTY, MINIMUM, MAXIMUM, True, self.getSelectedColor(), self.board.TOTAL_PIECES, self.board.BLACK_PIECES, self.board.WHITE_PIECES)
                # We append the key and value to temp_AI_Values
                temp_AI_values.update({key: value})
            # We reorder the temp values, so the highest flipped moves are at the end of the list. This is incase we get values that are equal to each other
            ordered_temp_values = dict(reversed(list(temp_AI_values.items())))
            # We loop through the keys, and find the highest value from the dictionary
            for key in ordered_temp_values:
                if(temp_AI_values[key] >= temp_value):
                    temp_value = temp_AI_values[key]
                    temp_key = key
            # We print debugAI
            self.debugAI(temp_AI_values)
            # We print the board states
            self.selected_player.getBoardStates()
            # We get the x and y piece of the key and add a piece to the board
            x = temp_key[0]
            y = temp_key[1]
            self.addPiece(x,y)
            # We print what color the AI is and what move it played.
            print("AI {} PLAYS {}".format(self.selected_player.getColor(), temp_key))
            # We update the board and score with this play
            self.playerPlayed(temp_key)
        # we reset the invalid checks since someone did play
        self.resetInvalid()
        # We draw the valid moves
        self.drawValidMoves()
    
    # drawValidMoves - draw the valid moves of the curent board state
    def drawValidMoves(self):
        for key in self.valid_moves:
            x_0 = key[0]
            y_1 = key[1]
            self.board.drawValidMoveCircle(x_0,y_1)

    # playerPlayed - updates the canvas with the move the current player played.
    def playerPlayed(self, play_move):
        self.flipTiles(play_move)
        self.update()
        self.currentScore()
        if(self.gameOver()):
            print("GAME OVER!")
            if(self.board.BLACK_PIECES > self.board.WHITE_PIECES):
                print("BLACK_WINS!!")
            elif(self.board.WHITE_PIECES > self.board.BLACK_PIECES):
                print("WHITE WINS!!")
            else:
                print("DRAW!!")
            self.root.quit()
            exit()
        self.change_turn()
        self.playTurn()

    # generateKeysList - We generate a list of keys to loop though.
    def generateKeysList(self):
        x = self.valid_moves.keys()
        for key in x:
            self.KEYS_LIST.append(key)
    
    # currentScore - prints the current score of the board
    def currentScore(self):
        print("Current score: Black: {} \t White {} \t {} TOTAL_PIECES: ".format(self.board.BLACK_PIECES, self.board.WHITE_PIECES, self.board.TOTAL_PIECES))
    
    # getValidMoves - prints the valid moves of the color
    def getValidMoves(self):
        print("{} valid moves".format(self.getSelectedColor()))
        for key in self.valid_moves:
            print("{} : {} flips".format(key, len(self.valid_moves[key])))
    
    # addPiece - adds a Piece to the board
    def addPiece(self, row, col):
        self.board.addPiece(row, col, self.getSelectedColor())

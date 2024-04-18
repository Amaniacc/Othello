# IMPORTS
from tkinter import *
from Game import *
from AI import *

# leftKeyPressed - Checks and see if the left key is pressed. If it is, it changes the available moves the player
# has to the one to the left of the list.

def leftKeyPressed(event):
    # Delete the current highlighted square.
    game.board.canvas.delete(HIGHLIGHT)
    # Get the current index of the list
    index = game.getCurrentIndex()
    # Since we are moving left, we check and see if we are at the begging of the list, if we are we need to return the
    # length of the list -1 to go to the end of the list. Else we decrement the index
    if(index == 0):
        index = len(game.KEYS_LIST)-1
    else:
        index -= 1

    # we update the current index to the new one
    game.updateCurrentIndex(index)
    # We get the value associated with this index
    values = game.KEYS_LIST[index]
    # We print the highlight square
    print("Highlighted Value = {}".format(values))
    # We draw the highlighted square
    values_x = values[0]
    values_y = values[1]
    if(game.getSelectedColor() == BLACK):
        game.board.canvas.create_rectangle(values_y * SQUARE_SIZE + SQUARE_SIZE, values_x * SQUARE_SIZE + SQUARE_SIZE, values_y * SQUARE_SIZE, values_x * SQUARE_SIZE, fill = YELLOW, tags=HIGHLIGHT)
    else:        
        game.board.canvas.create_rectangle(values_y * SQUARE_SIZE + SQUARE_SIZE, values_x * SQUARE_SIZE + SQUARE_SIZE, values_y * SQUARE_SIZE, values_x * SQUARE_SIZE, fill = ORANGE, tags=HIGHLIGHT)

# rightKeyPressed - Checks and see if the right key is pressed. If it is, it changes the available moves the palyer has
# to the one on the right of the list
def rightKeyPressed(event):
    # we delete the previously highlighted square.
    game.board.canvas.delete(HIGHLIGHT)
    # We get the index of the list
    index = game.getCurrentIndex()
    # Since we are moving right, if we hit the end of the list, we should return 0, stating we are going back to the
    # beginning of the list. Increment index otherwise.
    if(index == len(game.KEYS_LIST)-1):
        index = 0
    else:
        index += 1
    game.updateCurrentIndex(index)
    # We get the value associated with the index
    values = game.KEYS_LIST[index]

    # Print to say which piece is highted
    print("Highlighted Value = {}".format(values))

    # We draw the highlighted part on the board.
    values_x = values[0]
    values_y = values[1]
    if(game.getSelectedColor()== BLACK):
        game.board.canvas.create_rectangle(values_y * SQUARE_SIZE + SQUARE_SIZE, values_x * SQUARE_SIZE + SQUARE_SIZE, values_y * SQUARE_SIZE, values_x * SQUARE_SIZE, fill = YELLOW, tags=HIGHLIGHT)
    else:        
        game.board.canvas.create_rectangle(values_y * SQUARE_SIZE + SQUARE_SIZE, values_x * SQUARE_SIZE + SQUARE_SIZE, values_y * SQUARE_SIZE, values_x * SQUARE_SIZE, fill = ORANGE, tags=HIGHLIGHT)

# enterKeyPressed - Enter key has been pressed. It plays the move and draws the move on the canvas
def enterKeyPressed(event):
    # Gets the value at the index of the highlighted square
    playMove = game.KEYS_LIST[game.getCurrentIndex()]
    # Gets the x and y position of the value
    x = playMove[0]
    y = playMove[1]
    # adds the piece to the board
    game.addPiece(x,y)
    # calculates the changes of the move
    game.playerPlayed(playMove)

# Create the window and keys that will be associated with the game.
root = Tk()
game = Game(root, BLACK, AI(WHITE))
game.board.packBoard()
game.update()
game.playTurn()
game.currentScore()
root.bind("<Left>", leftKeyPressed)
root.bind("<Right>", rightKeyPressed)
root.bind("<Return>", enterKeyPressed)
root.mainloop()
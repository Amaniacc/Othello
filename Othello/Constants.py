'''
    Amani Cheatham
    102-81-556
    Due: November 13, 2022
    Assignment #3
    This program will Implement Othello, also known as Reversi, game with two players and an AI
    using the Mini-Max algorithm as well as alpha-beta pruning.
    This class will hold Global variables that will be used throughout all the files.
'''

# CONSTANTS
WIDTH,HEIGHT = 800, 800
ROWS,COLUMNS = 8,8
ROW_GAP, COLUMN_GAP = HEIGHT // ROWS, WIDTH // COLUMNS
SQUARE_SIZE = WIDTH//COLUMNS
DIFFICULTY = 4
MINIMUM = -999999
MAXIMUM = 999999

# COLOR PIECES
BLACK = "black"
WHITE = "white"
BLUE = "blue"
ASSIST = "assist"
YELLOW = "yellow"
ORANGE = "orange"
HIGHLIGHT = "highlight"

# BACKGROUND COLOR
BACKGROUND = "green"

# Directions
UP,DOWN,RIGHT,LEFT,UP_RIGHT,DOWN_RIGHT,DOWN_LEFT,UP_LEFT = (0,-1),(0,1),(1,0),(-1,0),(1,-1),(1,1),(-1,1),(-1,-1)
DIRECTIONS = [UP,DOWN,RIGHT,LEFT,UP_RIGHT,DOWN_RIGHT,DOWN_LEFT,UP_LEFT]
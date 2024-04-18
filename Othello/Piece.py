'''
    Amani Cheatham
    102-81-556
    Due: November 13, 2022
    Assignment #3
    This program will Implement Othello, also known as Reversi, game with two players and an AI
    using the Mini-Max algorithm as well as alpha-beta pruning.
    This is the piece class. This will control the objects placed on the board.
'''

# IMPORTS
from tkinter import *
from Constants import *

# Piece class
class Piece(object):
    PADDING = 10
    # It takes a row, col, and color of the piece
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

        # defines position on the board to draw the piece
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

        # define where on the board it will exist
        self.boardPosition()

    # boardPosition - defines in the canvas where the circle will exists.
    def boardPosition(self):
        x_center = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        y_center = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 2 - self.PADDING
        self.x0 = x_center - radius
        self.y0 = y_center - radius
        self.x1 = x_center + radius
        self.y1 = y_center + radius

    # getRow - returns the Row of Piece
    def getRow(self):
        return self.row
    
    # getCol - returns the Col of the Piece
    def getCol(self):
        return self.col
    
    # getColor - returns the color of the Piece
    def getColor(self):
        return self.color
    
    # updateColor - updates the color of the current piece
    def updateColor(self, value):
        self.color = value

    # draw - Draws piece on the canvas
    def draw(self, canvas):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill = self.color, outline = self.color)
    
    # __str__ - defines to python how we want to print this object.
    def __str__(self):
        return self.color

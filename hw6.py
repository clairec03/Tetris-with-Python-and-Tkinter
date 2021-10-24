#################################################
# hw6.py
#
# Your name: Claire Chen
# Your andrew id: ccz
#
# Your partner's name: Melinda Chen
# Your partner's andrew id: melindac
#################################################

import cs112_f21_week6_linter
import math, copy, random
from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def isPerfectSquare(n):
    factor = int(math.sqrt(n))
    return (factor**2==n)

def isSortOfSquarish(n):
    nonZeroDigits = list()
    if isPerfectSquare(n) or n < 0:
        return False
    # Uses this while loop to check for zero digits
    while n > 0:
        if n % 10 == 0:
            return False
        nonZeroDigits.append(n%10)
        # Truncate n by one digit to check for the next digit
        n //= 10
    # Creates a list of digits of n in the descending order to be added to the
    # result sortedN
    ascendingDigits = sorted(nonZeroDigits)
    descendingDigits = ascendingDigits[::-1]
    sortedN = 0
    # Adds digits raised to different powers of 10 to construct the final number
    for i in range(len(descendingDigits)):
        sortedN += descendingDigits[i] * 10 ** i
    if isPerfectSquare(sortedN):
        return True
    else: 
        return False

def nthSortOfSquarish(n):
    # Uses the search algorithm of count and guess, which is suitable for 
    # finding the "nth non-negative integer with some property"
    # Source: https://www.cs.cmu.edu/~112/notes/notes-loops.html
    found = 0
    guess = 0
    while found <= n: 
        if isSortOfSquarish(n):
            found += 1
        guess += 1
    # Subtracts one from the final result of guess because the last iteration
    # increments guess by 1 when count = n.
    return guess - 1

#################################################
# s21-midterm1-animation
#################################################

def s21MidtermAnimation_appStarted(app):
    app.cx = 0
    app.cy = 0
    app.dotColor = 'green'
    app.timerDelay = 5000
    app.radius = 20
    # Create a list of dots
    app.dots = list()
    # Keep track of the lines connecting the centers of dots
    # This list will include tuples that store four values:
    # Starting & ending coordinates (x0,y0,x1,y1)
    app.lines = list()

def s21MidtermAnimation_mousePressed(app, event):
    app.dots.append((event.x,event.y))
    if len(app.dots) > 1:
        app.lines.append((event.x,event.y,nearestDot(app,event)[0],
                                          nearestDot(app,event)[1]))

# def s21MidtermAnimation_timerFired(app):

def s21MidtermAnimation_redrawAll(app, canvas):
    for dot in app.dots:
        drawDot(dot,app,canvas)
    if len(app.dots) > 1:
        drawLine(app,canvas)

def drawDot(dot,app,canvas):
    canvas.create_oval(dot[0]-app.radius,dot[1]-app.radius,
                       dot[0]+app.radius, dot[1]+app.radius,fill='green')   

def drawLine(app,canvas):
    for line in app.lines:
        canvas.create_line(line[0], line[1],line[2], line[3])

def nearestDot(app,event):
    # Initialize the best distance to the distance between the first two dots
    # in the list. Similar to Q1 on HW 1, it uses the pythagorean theorem!
    bestDistance = math.sqrt((event.x-app.dots[0][0]) ** 2 + 
                             (event.y-app.dots[0][1]) ** 2)
    # Initialize the best dot to the first dot in the list of dots
    bestDot = (app.dots[0][0],app.dots[0][1])
    # Then, loop through all dots to see if the distance between the current dot
    # and another dot is smaller than bestDistance
    for i in range(len(app.dots)-1):
        distance = math.sqrt((event.x-app.dots[i][0]) ** 2 + 
                             (event.y-app.dots[i][1]) ** 2)
        if distance < bestDistance:
            # Update bestDistance and bestDot
            bestDistance = distance
            bestDot = (app.dots[i][0],app.dots[i][1])
    return bestDot

def s21Midterm1Animation():
    runApp(width=1000,height=1000, fnPrefix='s21MidtermAnimation_')

#################################################
# Tetris
#################################################

def appStarted(app):
    app.label = 'Tetris!'
    app.color = 'orange'
    app.emptyColor = 'blue'
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    # List comprehension! (line 148)
    # Source: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
    app.board = [(["blue"] * app.cols) for i in range(app.rows)]
    app.timerDelay = 500
    # Boolean flag for the entire game (initialized to false) and can 
    # stop the game by setting it equal to True
    app.isGameOver = False
    app.score = 0
    # Source:
    # https://www.cs.cmu.edu/~112/notes/notes-tetris/2_2_CreatingTheBoard.html
    # pre-load a few cells with known colors for testing purposes
    # app.board[0][0] = "red" # top-left is red
    # app.board[0][app.cols-1] = "white" # top-right is white
    # app.board[app.rows-1][0] = "green" # bottom-left is green
    # app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray
    # Seven "standard" pieces (tetrominoes)
    # Source: 
    # https://www.cs.cmu.edu/~112/notes/notes-tetris/
    # 2_3_CreatingTheFallingPiece.html
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False],[True, True, True]]
    lPiece = [[False, False, True],[True, True, True]]
    oPiece = [[True, True],[True, True]]
    sPiece = [[False, True, True],[True, True, False]]
    tPiece = [[False, True, False],[True, True, True]]
    zPiece = [[ True, True, False],[False, True, True]]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", 
                            "pink", "cyan", "green", "orange" ]
    newFallingPiece(app)

def timerFired(app):
    # Allows a new piece to fall if the game is not over
    if not app.isGameOver:
        # This condition allows the piece to be converted into the board
        if not moveFallingPiece(app, 1, 0):
            placeFallingPiece(app)
            for j in range(app.cols):
                # If the first row of the board has a piece of a block 
                # (which is not blue), then the game is over
                if app.board[0][j] != "blue":    
                    app.isGameOver = True
            newFallingPiece(app)

def gameDimensions():
    rows, cols, cellSize, margin = 15, 10, 20, 25
    return (rows, cols, cellSize, margin)

def keyPressed(app, event):
    # Restarts the game by pressing 'r'
    if app.isGameOver:
        if (event.key == 'r'):
            appStarted(app)
    # Source of keyPressed function: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1
    # .html#keyPressCounter
    if event.key == 'Space':
        hardDrop(app)
    elif (event.key == 'Left'):    
        moveFallingPiece(app, 0, -1)
    elif (event.key == 'Right'): 
        moveFallingPiece(app, 0, 1)
    elif (event.key == 'Up'):
        rotateFallingPiece(app)
    elif (event.key == 'Down'):
        moveFallingPiece(app, 1, 0)
    else:
        newFallingPiece(app)
    
def newFallingPiece(app):
    # Initialized the starting positions of new falling pieces
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    # Allow the falling piece to have a random color by choosing a random index
    # of the list of colors
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    numFallingPieceCols = len(app.fallingPiece[0])
    # Used integer division bc the number of cols and rows must be integers
    app.fallingPieceCol = app.cols // 2 - numFallingPieceCols // 2

def redrawAll(app, canvas):
    # Draws the falling piece and score count over the board
    drawBoard(app, canvas)
    drawFallingPiece(app,canvas) 
    if app.isGameOver: 
        drawGameOver(app,canvas) 
    drawScore(app,canvas) 

def drawGameOver(app,canvas):
    canvas.create_rectangle(app.margin,app.margin*2-6,
                            app.width-app.margin,
                            app.margin+3 * app.cellSize,fill = "black")
    canvas.create_text(app.margin+(app.cols/2)* app.cellSize,
                       app.margin + 2*app.cellSize,fill= 'yellow',
                       text='Game Over!',font = "Helvetica 28 bold")

def drawScore(app, canvas):
    # Uses the f-string method to print out the variable app.score
    canvas.create_text(app.margin+(app.cols/2) * app.cellSize,app.margin/2+1,
                       fill = 'blue', text=f'Score: {app.score}', 
                       font="Helvetica 12 bold")

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    width = 2 * margin + cellSize * cols
    height = 2 * margin + cellSize * rows
    runApp(width=width, height=height)

def drawBoard(app, canvas):
    # Fills the entire canvas with the orange background.
    x0, x1 = 0, app.width # Width: entire app
    y0, y1 = 0, app.height # Height: entire app
    canvas.create_rectangle(x0, y0, x1, y1, fill = "orange")
    # Then, draw the blue grid 
    # Loop through the rows and cols of the board to draw each individual cell
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j, app.board[i][j])

def drawCell(app, canvas, row, col, color):
    x0 = app.margin + col * app.cellSize
    x1 = x0 + app.cellSize # adds cellsize to the initial starting x coordinate
    y0 = app.margin + row * app.cellSize
    y1 = y0 + app.cellSize # adds cellsize to the initial starting y coordinate
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = 3)

def drawFallingPiece(app,canvas):
    if fallingPieceIsLegal(app):
        for i in range(len(app.fallingPiece)):
            for j in range(len(app.fallingPiece[0])):
                # True represents an element of the falling block,
                # which is drawn over the board
                if app.fallingPiece[i][j] == True:
                    drawCell(app,canvas,app.fallingPieceRow + i,
                    app.fallingPieceCol + j,app.fallingPieceColor)

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    # To set the bounds of the board,
    # undo a row/col change if the piece is not legal
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    else:
        return True

def fallingPieceIsLegal(app):
    row = len(app.fallingPiece)
    col = len(app.fallingPiece[0])
    for i in range(row):
        for j in range(col):
            if app.fallingPiece[i][j] == True:
                # This conditional checks if the falling piece is out of bounds
                if (app.fallingPieceRow + i > app.rows - 1
                or app.fallingPieceCol + j > app.cols - 1
                or app.fallingPieceRow + i < 0
                or app.fallingPieceCol + j < 0):
                    return False
                # Checks if the falling piece has landed on another piece
                if (app.board[app.fallingPieceRow+i][app.fallingPieceCol+j] != 
                                                                        "blue"):
                    return False
    # Returns True outside the for loop after verifying every element of 
    # the piece is legal
    return True

def rotateFallingPiece(app):
    oldRow = app.fallingPieceRow
    oldCol = app.fallingPieceCol
    oldPiece = app.fallingPiece
    oldNumRow = len(app.fallingPiece)
    oldNumCol = len(app.fallingPiece[0])
    # Rotation swaps the number of columns and rows
    newNumRow, newNumCol = oldNumCol, oldNumRow
    # Create a new list for the new piece so the location of the rotated
    # piece can be update without modifying the old list (non-destructive)
    newPiece = list()
    # Use list comprehension to generate the template list for the new Piece
    # Source: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
    newPiece += [([None] * newNumCol) for j in range(newNumRow)]
    for i in range(oldNumRow):
        for j in range(oldNumCol):
            newPiece[oldNumCol - j - 1][i] = oldPiece[i][j]
    # Source: 
    # https://www.cs.cmu.edu/~112/notes/notes-tetris
    # /2_5_RotatingTheFallingPiece.html
    newRow = oldRow + oldNumRow // 2 - newNumRow // 2
    newCol = oldCol + oldNumCol // 2 - newNumCol // 2
    # Set the old falling piece to the new falling piece after rotation
    app.fallingPieceRow, app.fallingPieceCol = newRow, newCol
    app.fallingPiece = newPiece
    # Check to see if the new piece is legal:
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow, app.fallingPieceCol = oldRow, oldCol
        app.fallingPiece = oldPiece

def hardDrop(app):
    while moveFallingPiece(app, 1, 0):
        continue

def placeFallingPiece(app):
    # Knowns: fallingPieceColor, app.fallingPiece, rows and cols of board
    if not app.isGameOver: # this boolean flag allows new pieces to be placed
                           # as long as the game is not over
        for i in range(len(app.fallingPiece)):
            for j in range(len(app.fallingPiece[0])):
                if app.fallingPiece[i][j] == True:
                    rowOfBoard = app.fallingPieceRow
                    colOfBoard = app.fallingPieceCol
                    # Turns the elements of the board from blue into the color
                    # of the falling piece if the piece is not falling
                    app.board[rowOfBoard+i][colOfBoard+j]=app.fallingPieceColor
    app.board = removeFullRows(app)

def removeFullRows(app):
    # To remove full rows of the board when needed, we need to create a list
    # called newBoard to modify the old board non-destructively
    newBoard = list()
    # Keeps track of fullRows and numOfFullRows
    fullRows = list()
    numOfFullRows = 0
    for i in range(app.rows):
        if isFullRow(app.board[i]):
            numOfFullRows += 1
            app.score += 1
            fullRows.append(app.board[i])
    # If no rows are full, we should not clear any row of the old board and 
    # just return the old board
    if numOfFullRows == 0:
        return app.board
    else:
        # Generates a new board using list comprehension:
        # Source: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
        # This appends blue / empty rows to the top of the board
        newBoard += [(["blue"] * app.cols) for i in range(numOfFullRows)]
        for i in range(app.rows):
            # Adds any non-full rows to the board, below the empty (blue) rows
            if app.board[i] not in fullRows:
                newBoard += [app.board[i]]
    return newBoard

# Helper function for removeFullRows
def isFullRow(rowOfBoard):
    if "blue" in rowOfBoard:
        return False
    # Returns true if there is no blue cell in the given row of the board
    else:
        return True

#################################################
# Test Functions
#################################################

def testIsPerfectSquare():
    print('Testing isPerfectSquare(n))...', end='')
    assert(isPerfectSquare(4) == True)
    assert(isPerfectSquare(9) == True)
    assert(isPerfectSquare(10) == False)
    assert(isPerfectSquare(225) == True)
    assert(isPerfectSquare(1225) == True)
    assert(isPerfectSquare(1226) == False)
    print('Passed')

def testIsSortOfSquarish():
    print('Testing isSortOfSquarish(n))...', end='')
    assert(isSortOfSquarish(52) == True)
    assert(isSortOfSquarish(16) == False)
    assert(isSortOfSquarish(502) == False)
    assert(isSortOfSquarish(414) == True)
    assert(isSortOfSquarish(5221) == True)
    assert(isSortOfSquarish(6221) == False)
    assert(isSortOfSquarish(-52) == False)
    print('Passed')

def testNthSortOfSquarish():
    print('Testing nthSortOfSquarish()...', end='')
    assert(nthSortOfSquarish(0) == 52)
    assert(nthSortOfSquarish(1) == 61)
    assert(nthSortOfSquarish(2) == 63)
    assert(nthSortOfSquarish(3) == 94)
    assert(nthSortOfSquarish(4) == 252)
    assert(nthSortOfSquarish(8) == 522)
    print('Passed')

def testAll():
    testIsPerfectSquare()
    testIsSortOfSquarish()
    testNthSortOfSquarish()

#################################################
# main
#################################################

def main():
    cs112_f21_week6_linter.lint()
    s21Midterm1Animation()
    playTetris()
    testAll()

if __name__ == '__main__':
    main()
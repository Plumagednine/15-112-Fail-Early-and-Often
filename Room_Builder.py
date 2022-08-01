from cmu_112_graphics import *
from helpers import print2dList

def appStarted(app):
    app.rows = 16
    app.cols = 16
    app.margin = 5 # margin around grid
    app.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    app.grid = [[0 for col in range(app.cols)] for row in range(app.rows)]
    

def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def mousePressed(app, event):
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if app.grid[row][col] < 6:
        app.grid[row][col] += 1
    else:
        app.grid[row][col] = 0
        
def keyPressed(app, event):
    if event.key == 'e':
        print("#############################")
        print2dList(app.grid)
        print("#############################")
    elif event.key == 'r':
        app.grid = [[0 for col in range(app.cols)] for row in range(app.rows)]

def drawRoom(app, canvas):
    gridSize = 16
    gridLayout = app.grid
    for row in range(gridSize):
        for col in range(gridSize):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if gridLayout[row][col] == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
            elif gridLayout[row][col] == 1:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 1)
            elif gridLayout[row][col] == 2:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#1b4965', width = 1)
            elif gridLayout[row][col] == 3:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#6C7D47', width = 1)
            elif gridLayout[row][col] == 4:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#8E8686', width = 1)
            elif gridLayout[row][col] == 5:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#FE6D73', width = 1)
            elif gridLayout[row][col] == 6:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#E09F3E', width = 1)
                

def redrawAll(app, canvas):
    # draw grid of cells
    drawRoom(app, canvas)

runApp(width=400, height=400)
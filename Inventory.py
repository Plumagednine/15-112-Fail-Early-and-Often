from cmu_112_graphics import *


class Inventory:
    def __init__(app, gridSize):
        app.gridSize = gridSize
    
    def getSize(app):
        return app.gridSize
    
    def getLayout(app):
        return app.grid
    
    def getSpawnPoint(app):
        for row in range(app.gridSize):
            for col in range(app.gridSize):
                if app.grid[row][col] == 2:
                    return (row, col)
    
    def getEndPoint(app):
        for row in range(app.gridSize):
            for col in range(app.gridSize):
                if app.grid[row][col] == 3:
                    return (row, col)
    
    def updateGrid(app, row, col, value):
        app.grid[row][col] = value
        return app.grid
        
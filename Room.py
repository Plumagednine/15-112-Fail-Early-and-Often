from cmu_112_graphics import *
import random
from Monster import *
from Items import *

class Room:
    def __init__(self, roomDict):
        self.name = roomDict.get("roomName")
        self.id = roomDict.get("roomId")
        self.grid = roomDict.get("roomLayout")
        self.gridSize = len(self.grid)
        pass
    
    def drawRoom(self, app, canvas):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                (x0, y0, x1, y1) = getCellBounds(row, col, app.gridWidth, app.gridHeight, gridSize)
                if gridLayout[row][col] == 0:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
                elif gridLayout[row][col] == 1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 1)
                elif gridLayout[row][col] == 2:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1b4965', width = 1)
                elif gridLayout[row][col] == 3:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#6C7D47', width = 1)
    pass

    def drawRoom(self, app, canvas):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                (x0, y0, x1, y1) = getCellBounds(row, col, app.gridWidth, app.gridHeight, gridSize)
                if gridLayout[row][col] == 1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 1)
                elif gridLayout[row][col] == 2:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1b4965', width = 1)
                elif gridLayout[row][col] == 3:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#6C7D47', width = 1)
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
        pass
        
    def getSize(self):
        return self.gridSize
    
    def getLayout(self):
        return self.grid
    
    def updateGrid(self, row, col, value):
        self.grid[row][col] = value
        return self.grid
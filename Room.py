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
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col] == 2:
                    self.playerSpawn = (row, col)
                elif self.grid[row][col] == 3:
                    self.playerExit = (row, col)
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
                elif gridLayout[row][col] == 4:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#8E8686', width = 1)
    pass

    def getPlayerSpawn(self):
        return self.playerSpawn
        
    def getEndPoint(self):
        return self.playerExit
        
    def getSize(self):
        return self.gridSize
    
    def getLayout(self):
        return self.grid
    
    def updateGrid(self, row, col, value):
        self.grid[row][col] = value
        return self.grid
    
    def setWall(self, wall):
        #0 == top, 1 == left, 2 == bottom, 3 == right
        if wall == 0:
            for i in range(0,self.gridSize):
                if self.grid[0][i] == 0:
                    self.updateGrid(0, i, 4)
            pass
        elif wall == 1:
            for i in range(0,self.gridSize):
                if self.grid[i][0] == 0:
                    self.updateGrid(i,0, 4)
            pass
        elif wall == 2:
            for i in range(0,self.gridSize):
                if self.grid[self.gridSize-1][i] == 0:
                    self.updateGrid(self.gridSize-1, i, 4)
            pass
        elif wall == 3:
            for i in range(0,self.gridSize):
                if self.grid[i][self.gridSize-1] == 0:
                    self.updateGrid(i, self.gridSize-1, 4)
            pass
      
        
from cmu_112_graphics import *
import random
from Monster import *
from Items import *
from helpers import *

class Room:
    def __init__(self, app, roomDict, allItems, allMonsters):
        self.name = roomDict.get("roomName")
        self.id = roomDict.get("roomId")
        self.grid = roomDict.get("roomLayout")
        self.gridSize = len(self.grid)
        self.allItems = allItems
        self.allWeapons = {}
        self.allArmor = {}
        self.allMiscItems = {}
        for item in allItems:
            tempItem = allItems.get(item)
            if tempItem.getItemType() == "Weapon":
                self.allWeapons[item] = allItems.get(item)
            elif tempItem.getItemType() == "Armor":
                self.allArmor[item] = allItems.get(item)
            elif tempItem.getItemType() == "MiscItem":
                self.allMiscItems[item] = allItems.get(item)
        self.allItemsList = [self.allWeapons, self.allArmor, self.allMiscItems]
        self.allMonsters = allMonsters
        # app.gridWidth = app.width-int(app.height*.5)
        # app.gridHeight = app.height
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col] == 2:
                    self.playerSpawn = (row, col)
                elif self.grid[row][col] == 3:
                    self.playerExit = (row, col)
                elif self.grid[row][col] == 5:
                    tempMonster = copy.deepcopy(self.allMonsters.get(random.choice(list(self.allMonsters))))
                    spriteSheet = tempMonster.sprites
                    tempMonster.sprites = animateSprite(app, spriteSheet, app.gridWidth, app.gridHeight, self.gridSize) 
                    tempMonster.setRoomPos(row, col)
                    self.grid[row][col] = tempMonster
                elif self.grid[row][col] == 6:
                    tempItem = copy.deepcopy(self.allItems.get(random.choice(list(random.choice(self.allItemsList)))))
                    itemImage = app.loadImage(tempItem.itemImage)
                    itemImage = resizeSprite(itemImage, app.gridWidth//self.gridSize, app.gridHeight//self.gridSize)
                    tempItem.itemImage = itemImage
                    self.grid[row][col] = tempItem
                    
        pass
    
    def drawRoom(self, app, canvas):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                (x0, y0, x1, y1) = getCellBounds(row, col, app.gridWidth, app.gridHeight, gridSize)
                canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
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
                elif isinstance(gridLayout[row][col],Items):
                    canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, image = ImageTk.PhotoImage(gridLayout[row][col].getItemImage()))
                elif isinstance(gridLayout[row][col],Monster):
                    gridLayout[row][col].drawMonster(app, canvas, self.gridSize)
                    
    def animateRoom(self):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                if isinstance(gridLayout[row][col],Monster):
                    gridLayout[row][col].animateSprite()
                    
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
        
    def tick(self, playerPos):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if isinstance(self.grid[row][col],Monster):
                    self.grid[row][col].tick(playerPos, self.getLayout())
      
        
import decimal
from cmu_112_graphics import *
import random
import copy
from helpers import *
from Room import *

# This class is used to generate a level for the game.
# """
# It generates a maze, fills it with rooms, and sets the surrounding walls of each room.

# :param allRoomsDictionary: a dictionary of all the rooms in the game. The keys are the room
# numbers, and the values are the room objects
# :param gridSize: the size of the grid, defaults to 16 (optional)
# """
class level_generation:
    def setSurroundingWalls(self, row, col):
        if self.grid[row-1][col] == 1:
                    self.grid[row][col].setWall(0)
        if self.grid[row][col-1] == 1:
                    self.grid[row][col].setWall(1)
        if self.grid[row+1][col] == 1:
                    self.grid[row][col].setWall(2)
        if self.grid[row][col+1] == 1:
                    self.grid[row][col].setWall(3)
        pass
    #######################################
    ###Initalizer Function#################
    #######################################
    def __init__(self, allRoomsDictionary, gridSize = 16,):
        self.allRooms = allRoomsDictionary
        self.gridSize = gridSize
        self.grid=[]
        self.gridRow=[]
        self.spawnPoint = random.randint(0,gridSize-1), random.randint(0,gridSize-1)
        self.endpoint = self.spawnPoint
        #######################################
        ###Generating Maze Code################
        #######################################
        startingRow, startingCol = self.spawnPoint
        for col in range(self.gridSize):
            for row in range(self.gridSize):
                self.gridRow.append('empty')
            self.grid.append(self.gridRow)
            self.gridRow=[]
        
        # make border around map
        if startingRow == 0:
            startingRow += 1
        if startingRow == self.gridSize-1:
            startingRow -= 1
        if startingCol == 0:
            startingCol += 1
        if startingCol == self.gridSize-1:
            startingCol -= 1
        
        # make starting point a hallway
        self.grid[startingRow][startingCol] = 0
                
        # get cells surrounding starting position and set them to a wall
        walls = []
        walls.append([startingRow-1, startingCol])
        walls.append([startingRow, startingCol-1])
        walls.append([startingRow, startingCol+1])
        walls.append([startingRow+1, startingCol])
        self.grid[startingRow-1][startingCol] = 1
        self.grid[startingRow][startingCol-1] = 1
        self.grid[startingRow][startingCol+1] = 1
        self.grid[startingRow+1][startingCol] = 1
        
        #get the number of hallways around the cell that we are going from
        def surroundingCells(currentCell):
            surroundingHallways = 0
            if (self.grid[currentCell[0]-1][currentCell[1]] == 0):
                surroundingHallways += 1
            if (self.grid[currentCell[0]+1][currentCell[1]] == 0):
                surroundingHallways += 1
            if (self.grid[currentCell[0]][currentCell[1]-1] == 0):
                surroundingHallways += 1
            if (self.grid[currentCell[0]][currentCell[1]+1] == 0):
                surroundingHallways += 1
            return surroundingHallways
        
        def getWallType(workingWall):
            #is top wall
            if (workingWall[0] != 0):
                if (self.grid[workingWall[0]-1][workingWall[1]] == 'empty' and self.grid[workingWall[0]+1][workingWall[1]] == 0):
                    return "top wall"
                
            #is bottom wall
            if (workingWall[0] != self.gridSize-1):
                if (self.grid[workingWall[0]+1][workingWall[1]] == 'empty' and self.grid[workingWall[0]-1][workingWall[1]] == 0):
                    return "bottom wall"
            
            #is left wall
            if (workingWall[1] != 0):
                if (self.grid[workingWall[0]][workingWall[1]-1] == 'empty' and self.grid[workingWall[0]][workingWall[1]+1] == 0):
                    return "left wall"
            
            #is right wall
            if (workingWall[1] != self.gridSize-1):
                if (self.grid[workingWall[0]][workingWall[1]+1] == 'empty' and self.grid[workingWall[0]][workingWall[1]-1] == 0):
                    return "right wall"
            
        def setTopWall(workingWall):
            # Upper wall
            if (workingWall[0] != 0):
                if (self.grid[workingWall[0]-1][workingWall[1]] != 0):
                    self.grid[workingWall[0]-1][workingWall[1]] = 1
        
        def setBottomWall(workingWall):
            # Bottom wall
            if (workingWall[0] != self.gridSize-1):
                if (self.grid[workingWall[0]+1][workingWall[1]] != 0):
                    self.grid[workingWall[0]+1][workingWall[1]] = 1
        
        def setLeftWall(workingWall):
            # Leftmost cell
            if (workingWall[1] != 0):
                if (self.grid[workingWall[0]][workingWall[1]-1] != 0):
                    self.grid[workingWall[0]][workingWall[1]-1] = 1
        
        def setRightWall(workingWall):
            # Rightmost cell
            if (workingWall[1] != self.gridSize-1):
                if (self.grid[workingWall[0]][workingWall[1]+1] != 0):
                    self.grid[workingWall[0]][workingWall[1]+1] = 1
                    
        while (walls):
            # Pick a random wall
            workingWall = walls[int(random.random()*len(walls))-1]
            
            # Check top wall
            if (getWallType(workingWall) == "top wall"):
                #get the number of surrounding hallways
                surroundingHallways = surroundingCells(workingWall)
                # if there are less than 2 paths
                if (surroundingHallways <= 1):
                    # set position as hallway
                    self.grid[workingWall[0]][workingWall[1]] = 0
                    
                    #set touching walls
                    setTopWall(workingWall)
                    if ([workingWall[0]-1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]-1, workingWall[1]])
                    setLeftWall(workingWall)
                    if ([workingWall[0], workingWall[1]-1] not in walls):
                        walls.append([workingWall[0], workingWall[1]-1])
                    setRightWall(workingWall)
                    if ([workingWall[0], workingWall[1]+1] not in walls):
                        walls.append([workingWall[0], workingWall[1]+1])
                        
                # Delete wall
                for wall in walls:
                    if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                        walls.remove(wall)
                continue
            
            # Check bottom wall
            if (getWallType(workingWall) == "bottom wall"):
                #get the number of surrounding hallways
                surroundingHallways = surroundingCells(workingWall)
                # if there are less than 2 paths
                if (surroundingHallways <= 1):
                    #set position as hallway
                    self.grid[workingWall[0]][workingWall[1]] = 0
                    
                    # set touching walls
                    setBottomWall(workingWall)
                    if ([workingWall[0]+1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]+1, workingWall[1]])
                    setLeftWall(workingWall)
                    if ([workingWall[0], workingWall[1]-1] not in walls):
                        walls.append([workingWall[0], workingWall[1]-1])
                    setRightWall(workingWall)
                    if ([workingWall[0], workingWall[1]+1] not in walls):
                        walls.append([workingWall[0], workingWall[1]+1])
                        
                # Delete wall
                for wall in walls:
                    if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                        walls.remove(wall)
                continue
              
            # Check left wall
            if (getWallType(workingWall) == "left wall"):
                #get the number of surrounding hallways
                surroundingHallways = surroundingCells(workingWall)
                # if there are less than 2 paths
                if (surroundingHallways <= 1):
                    # set position as hallway
                    self.grid[workingWall[0]][workingWall[1]] = 0
                    
                    #set touching walls
                    setTopWall(workingWall)
                    if ([workingWall[0]-1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]-1, workingWall[1]])
                    setBottomWall(workingWall)
                    if ([workingWall[0]+1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]+1, workingWall[1]])
                    setLeftWall(workingWall)
                    if ([workingWall[0], workingWall[1]-1] not in walls):
                        walls.append([workingWall[0], workingWall[1]-1])
                        
                # Delete wall
                for wall in walls:
                    if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                        walls.remove(wall)
                continue
            
            # Check right wall
            if (getWallType(workingWall) == "right wall"):
                #get the number of surrounding hallways
                surroundingHallways = surroundingCells(workingWall)
                # if there are less than 2 paths
                if (surroundingHallways <= 1):
                    # set position as hallway
                    self.grid[workingWall[0]][workingWall[1]] = 0
                    
                    #set touching walls
                    setTopWall(workingWall)
                    if ([workingWall[0]-1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]-1, workingWall[1]])
                    setBottomWall(workingWall)
                    if ([workingWall[0]+1, workingWall[1]] not in walls):
                        walls.append([workingWall[0]+1, workingWall[1]])
                    setRightWall(workingWall)
                    if ([workingWall[0], workingWall[1]+1] not in walls):
                        walls.append([workingWall[0], workingWall[1]+1])
                        
                # Delete wall
                for wall in walls:
                    if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                        walls.remove(wall)
                continue

            # Delete leftovers
            for wall in walls:
                if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                    walls.remove(wall)
            
        
        
        #######################################
        ###Clean Up Maze#######################
        #######################################
        
        # Mark the remaining unvisited cells as walls
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if (self.grid[i][j] == 'empty'):
                    self.grid[i][j] = 1
                    
        #setup start and endpoints and make sure they are not too close to each other
        self.grid[startingRow][startingCol] = 2
        endingRow, endingCol = startingRow, startingCol
        while (endingRow, endingCol) == (startingRow, startingCol):
            tempEndingRow, tempEndingCol = random.randint(0, self.gridSize-1), random.randint(0, self.gridSize-1)
            if ((tempEndingCol-startingCol)**2 + (tempEndingRow-startingRow)**2)**0.5 > gridSize//2:
                if self.grid[tempEndingRow][tempEndingCol] == 0:
                    endingRow, endingCol = tempEndingRow, tempEndingCol
        self.grid[endingRow][endingCol] = 3
        
        #######################################
        ###Fill With Rooms#####################
        #######################################
        for row in range(0, self.gridSize):
            for col in range(0, self.gridSize):
                if (self.grid[row][col] == 0):
                    tempRoom = copy.deepcopy(self.allRooms.get(random.randint(0, len(self.allRooms)-3)))
                    self.grid[row][col] = tempRoom
                elif (self.grid[row][col] == 2):
                    self.spawnPoint = (row, col)
                    self.grid[row][col] = copy.deepcopy(self.allRooms.get(-1))
                elif (self.grid[row][col] == 3):
                    self.endpoint = (row, col)
                    self.grid[row][col] = copy.deepcopy(self.allRooms.get(-2))
                if self.grid[row][col] != 1:
                    self.setSurroundingWalls(row, col)
                
        #######################################
        ###End INIT############################
        #######################################

    def drawDungeon(self, app, canvas):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                (x0, y0, x1, y1) = getCellBounds(row, col, app.gridWidth, app.gridHeight, gridSize)
                if gridLayout[row][col] == 1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 1)
                elif gridLayout[row][col].id == -1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1b4965', width = 1)
                elif gridLayout[row][col].id == -2:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#6C7D47', width = 1)
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
        pass
    
    def getRoom(self, row, col):
        return self.grid[row][col]
    
    def getSize(self):
        return self.gridSize
    
    def getLayout(self):
        return self.grid
    
    def getSpawnPoint(self):
        return self.spawnPoint
    
    def getEndPoint(self):
        return self.endpoint
    
    def updateGrid(self, row, col, value):
        self.grid[row][col] = value
        return self.grid
    
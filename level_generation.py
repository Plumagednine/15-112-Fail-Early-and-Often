from cmu_112_graphics import *
import random

class level_generation:
    def __init__(self, gridSize = 5):
        self.gridSize = gridSize
        self.grid=[]
        self.gridRow=[]
        self.spawnPoint = random.randint(0,gridSize-1), random.randint(0,gridSize-1)
        ##################################################################################################
        ##########Generating Maze Code####################################################################
        ##################################################################################################
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
            
        
        ##################################################################################################
        ##########Clean Up Maze###########################################################################
        ##################################################################################################
        
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
        pass
        
        ##################################################################################################
        ##########End INIT################################################################################
        ##################################################################################################

    def getSize(self):
        return self.gridSize
    
    def getLayout(self):
        return self.grid
    
    def getSpawnPoint(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col] == 2:
                    return (row, col)
    
    def getEndPoint(self):
        for row in range(self.gridSize):
            for col in range(self.gridSize):
                if self.grid[row][col] == 3:
                    return (row, col)
    
    def updateGrid(self, row, col, value):
        self.grid[row][col] = value
        return self.grid
    
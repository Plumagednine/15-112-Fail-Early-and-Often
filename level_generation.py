import decimal
from cmu_112_graphics import *
import random

class level_generation:
    #######################################
    ###Helper Functions####################
    #######################################

    def almostEqual(self, d1, d2, epsilon=10**-7): #helper-fn
        # note: use math.isclose() outside 15-112 with Python version 3.5 or later
        return (abs(d2 - d1) < epsilon)

    def roundHalfUp(self, d): #helper-fn
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def create_elipse(self, canvas, cx, cy, radius, **options):
        canvas.create_oval(cx - radius
                        , cy - radius
                        , cx + radius
                        , cy + radius
                        , **options)

    def getCell(self, x, y, width, height, gridSize):
        cellWidth = width // gridSize
        cellHeight = height // gridSize
        row =  y//cellHeight
        col = x//cellWidth
        return (row, col)

    def getCellBounds(self, row, col, width, height, gridSize):
        cellWidth = width // gridSize
        cellHeight = height // gridSize
        x0 = col * cellWidth
        y0 = row * cellHeight
        x1 = (col+1) * cellWidth
        y1 = (row+1) * cellHeight
        return (x0, y0, x1, y1)

    #######################################
    ###Initalizer Function#################
    #######################################
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

    def drawDungeon(self, app, canvas):
        gridSize = self.getSize()
        gridLayout = self.getLayout()
        for row in range(gridSize):
            for col in range(gridSize):
                (x0, y0, x1, y1) = self.getCellBounds(row, col, app.gridWidth, app.gridHeight, gridSize)
                if gridLayout[row][col] == 0:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 1)
                elif gridLayout[row][col] == 1:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 1)
                elif gridLayout[row][col] == 2:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#1b4965', width = 1)
                elif gridLayout[row][col] == 3:
                    canvas.create_rectangle(x0, y0, x1, y1, fill='#6C7D47', width = 1)
        pass
    
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
    
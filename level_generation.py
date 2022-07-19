from cmu_112_graphics import *
import random

class level_generation:
    def __init__(app, gridSize = 5):
        app.gridSize = gridSize
        app.grid=[]
        app.gridRow=[]
        app.spawnPoint = random.randint(0,gridSize-1), random.randint(0,gridSize-1)
        ##################################################################################################
        ##########Generating Maze Code####################################################################
        ##################################################################################################
        startingRow, startingCol = app.spawnPoint
        for col in range(app.gridSize):
            for row in range(app.gridSize):
                app.gridRow.append('empty')
            app.grid.append(app.gridRow)
            app.gridRow=[]
        
        # make border around map
        if startingRow == 0:
            startingRow += 1
        if startingRow == app.gridSize-1:
            startingRow -= 1
        if startingCol == 0:
            startingCol += 1
        if startingCol == app.gridSize-1:
            startingCol -= 1
        
        # make starting point a hallway
        app.grid[startingRow][startingCol] = 0
                
        # get cells surrounding starting position and set them to a wall
        walls = []
        walls.append([startingRow-1, startingCol])
        walls.append([startingRow, startingCol-1])
        walls.append([startingRow, startingCol+1])
        walls.append([startingRow+1, startingCol])
        app.grid[startingRow-1][startingCol] = 1
        app.grid[startingRow][startingCol-1] = 1
        app.grid[startingRow][startingCol+1] = 1
        app.grid[startingRow+1][startingCol] = 1
        
        #get the number of hallways around the cell that we are going from
        def surroundingCells(currentCell):
            surroundingHallways = 0
            if (app.grid[currentCell[0]-1][currentCell[1]] == 0):
                surroundingHallways += 1
            if (app.grid[currentCell[0]+1][currentCell[1]] == 0):
                surroundingHallways += 1
            if (app.grid[currentCell[0]][currentCell[1]-1] == 0):
                surroundingHallways += 1
            if (app.grid[currentCell[0]][currentCell[1]+1] == 0):
                surroundingHallways += 1
            return surroundingHallways
        
        def getWallType(workingWall):
            #is top wall
            if (workingWall[0] != 0):
                if (app.grid[workingWall[0]-1][workingWall[1]] == 'empty' and app.grid[workingWall[0]+1][workingWall[1]] == 0):
                    return "top wall"
                
            #is bottom wall
            if (workingWall[0] != app.gridSize-1):
                if (app.grid[workingWall[0]+1][workingWall[1]] == 'empty' and app.grid[workingWall[0]-1][workingWall[1]] == 0):
                    return "bottom wall"
            
            #is left wall
            if (workingWall[1] != 0):
                if (app.grid[workingWall[0]][workingWall[1]-1] == 'empty' and app.grid[workingWall[0]][workingWall[1]+1] == 0):
                    return "left wall"
            
            #is right wall
            if (workingWall[1] != app.gridSize-1):
                if (app.grid[workingWall[0]][workingWall[1]+1] == 'empty' and app.grid[workingWall[0]][workingWall[1]-1] == 0):
                    return "right wall"
            
        def setTopWall(workingWall):
            # Upper wall
            if (workingWall[0] != 0):
                if (app.grid[workingWall[0]-1][workingWall[1]] != 0):
                    app.grid[workingWall[0]-1][workingWall[1]] = 1
        
        def setBottomWall(workingWall):
            # Bottom wall
            if (workingWall[0] != app.gridSize-1):
                if (app.grid[workingWall[0]+1][workingWall[1]] != 0):
                    app.grid[workingWall[0]+1][workingWall[1]] = 1
        
        def setLeftWall(workingWall):
            # Leftmost cell
            if (workingWall[1] != 0):
                if (app.grid[workingWall[0]][workingWall[1]-1] != 0):
                    app.grid[workingWall[0]][workingWall[1]-1] = 1
        
        def setRightWall(workingWall):
            # Rightmost cell
            if (workingWall[1] != app.gridSize-1):
                if (app.grid[workingWall[0]][workingWall[1]+1] != 0):
                    app.grid[workingWall[0]][workingWall[1]+1] = 1
                    
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
                    app.grid[workingWall[0]][workingWall[1]] = 0
                    
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
                    app.grid[workingWall[0]][workingWall[1]] = 0
                    
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
                    app.grid[workingWall[0]][workingWall[1]] = 0
                    
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
                    app.grid[workingWall[0]][workingWall[1]] = 0
                    
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
        for i in range(0, app.gridSize):
            for j in range(0, app.gridSize):
                if (app.grid[i][j] == 'empty'):
                    app.grid[i][j] = 1
                    
        #setup start and endpoints and make sure they are not too close to each other
        app.grid[startingRow][startingCol] = 2
        endingRow, endingCol = startingRow, startingCol
        while (endingRow, endingCol) == (startingRow, startingCol):
            tempEndingRow, tempEndingCol = random.randint(0, app.gridSize-1), random.randint(0, app.gridSize-1)
            if ((tempEndingCol-startingCol)**2 + (tempEndingRow-startingRow)**2)**0.5 > gridSize//2:
                if app.grid[tempEndingRow][tempEndingCol] == 0:
                    endingRow, endingCol = tempEndingRow, tempEndingCol
        app.grid[endingRow][endingCol] = 3
        pass
        
        ##################################################################################################
        ##########End INIT################################################################################
        ##################################################################################################

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

grid = level_generation(6)
print(grid.getLayout())
    
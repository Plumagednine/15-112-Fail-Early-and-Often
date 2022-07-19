import random
from cmu_112_graphics import *

class level_gen:
    def __init__(app, gridSize = 5):
            app.gridSize = gridSize
            app.grid=[]
            app.gridRow=[]
            cell = 0
            wall = 1
            app.spawnPoint = random.randint(0,gridSize-1), random.randint(0,gridSize-1)
            ####################################################################################################################################################
            ################################Generating Maze Code################################################################################################
            ####################################################################################################################################################
            startingRow, startingCol = app.spawnPoint
            for col in range(app.gridSize):
                for row in range(app.gridSize):
                    app.gridRow.append('empty')
                app.grid.append(app.gridRow)
                app.gridRow=[]
            if startingRow == 0:
                startingRow = startingRow + 1
            if startingRow == app.gridSize-1:
                startingRow = startingRow - 1
            if startingCol == 0:
                startingCol = startingCol + 1
            if startingCol == app.gridSize-1:
                startingCol = startingCol - 1
            app.grid[startingRow][startingCol] = cell
            walls = []
            walls.append([startingRow-1, startingCol])
            walls.append([startingRow, startingCol-1])
            walls.append([startingRow, startingCol+1])
            walls.append([startingRow+1, startingCol])
            app.grid[startingRow-1][startingCol] = wall
            app.grid[startingRow][startingCol-1] = wall
            app.grid[startingRow][startingCol+1] = wall
            app.grid[startingRow+1][startingCol] = wall
            
            def surroundingCells(workingWall):
                s_cells = 0
                if (app.grid[workingWall[0]-1][workingWall[1]] == 0):
                    s_cells += 1
                if (app.grid[workingWall[0]+1][workingWall[1]] == 0):
                    s_cells += 1
                if (app.grid[workingWall[0]][workingWall[1]-1] == 0):
                    s_cells +=1
                if (app.grid[workingWall[0]][workingWall[1]+1] == 0):
                    s_cells += 1
                return s_cells
            
            while (walls):
                # Pick a random wall
                workingWall = walls[int(random.random()*len(walls))-1]
                # Check if it is a left wall
                if (workingWall[1] != 0):
                    if (app.grid[workingWall[0]][workingWall[1]-1] == 'empty' and app.grid[workingWall[0]][workingWall[1]+1] == 0):
                        # Find the number of surrounding cells
                        s_cells = surroundingCells(workingWall)
                        if (s_cells < 2):
                            # Denote the new path
                            app.grid[workingWall[0]][workingWall[1]] = 0
                            # Mark the new walls
                            # Upper cell
                            if (workingWall[0] != 0):
                                if (app.grid[workingWall[0]-1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]-1][workingWall[1]] = 1
                                if ([workingWall[0]-1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]-1, workingWall[1]])
                            # Bottom cell
                            if (workingWall[0] != app.gridSize-1):
                                if (app.grid[workingWall[0]+1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]+1][workingWall[1]] = 1
                                if ([workingWall[0]+1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]+1, workingWall[1]])
                            # Leftmost cell
                            if (workingWall[1] != 0):	
                                if (app.grid[workingWall[0]][workingWall[1]-1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]-1] = 1
                                if ([workingWall[0], workingWall[1]-1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]-1])
                        # Delete wall
                        for wall in walls:
                            if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                                walls.remove(wall)
                        continue

                # Check if it is an upper wall
                if (workingWall[0] != 0):
                    if (app.grid[workingWall[0]-1][workingWall[1]] == 'empty' and app.grid[workingWall[0]+1][workingWall[1]] == 0):
                        s_cells = surroundingCells(workingWall)
                        if (s_cells < 2):
                            # Denote the new path
                            app.grid[workingWall[0]][workingWall[1]] = 0
                            # Mark the new walls
                            # Upper cell
                            if (workingWall[0] != 0):
                                if (app.grid[workingWall[0]-1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]-1][workingWall[1]] = 1
                                if ([workingWall[0]-1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]-1, workingWall[1]])
                            # Leftmost cell
                            if (workingWall[1] != 0):
                                if (app.grid[workingWall[0]][workingWall[1]-1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]-1] = 1
                                if ([workingWall[0], workingWall[1]-1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]-1])
                            # Rightmost cell
                            if (workingWall[1] != app.gridSize-1):
                                if (app.grid[workingWall[0]][workingWall[1]+1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]+1] = 1
                                if ([workingWall[0], workingWall[1]+1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]+1])
                        # Delete wall
                        for wall in walls:
                            if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                                walls.remove(wall)
                        continue

                # Check the bottom wall
                if (workingWall[0] != app.gridSize-1):
                    if (app.grid[workingWall[0]+1][workingWall[1]] == 'empty' and app.grid[workingWall[0]-1][workingWall[1]] == 0):
                        s_cells = surroundingCells(workingWall)
                        if (s_cells < 2):
                            # Denote the new path
                            app.grid[workingWall[0]][workingWall[1]] = 0
                            # Mark the new walls
                            if (workingWall[0] != app.gridSize-1):
                                if (app.grid[workingWall[0]+1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]+1][workingWall[1]] = 1
                                if ([workingWall[0]+1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]+1, workingWall[1]])
                            if (workingWall[1] != 0):
                                if (app.grid[workingWall[0]][workingWall[1]-1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]-1] = 1
                                if ([workingWall[0], workingWall[1]-1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]-1])
                            if (workingWall[1] != app.gridSize-1):
                                if (app.grid[workingWall[0]][workingWall[1]+1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]+1] = 1
                                if ([workingWall[0], workingWall[1]+1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]+1])
                        # Delete wall
                        for wall in walls:
                            if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                                walls.remove(wall)
                        continue

                # Check the right wall
                if (workingWall[1] != app.gridSize-1):
                    if (app.grid[workingWall[0]][workingWall[1]+1] == 'empty' and app.grid[workingWall[0]][workingWall[1]-1] == 0):
                        s_cells = surroundingCells(workingWall)
                        if (s_cells < 2):
                            # Denote the new path
                            app.grid[workingWall[0]][workingWall[1]] = 0
                            # Mark the new walls
                            if (workingWall[1] != app.gridSize-1):
                                if (app.grid[workingWall[0]][workingWall[1]+1] != 0):
                                    app.grid[workingWall[0]][workingWall[1]+1] = 1
                                if ([workingWall[0], workingWall[1]+1] not in walls):
                                    walls.append([workingWall[0], workingWall[1]+1])
                            if (workingWall[0] != app.gridSize-1):
                                if (app.grid[workingWall[0]+1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]+1][workingWall[1]] = 1
                                if ([workingWall[0]+1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]+1, workingWall[1]])
                            if (workingWall[0] != 0):	
                                if (app.grid[workingWall[0]-1][workingWall[1]] != 0):
                                    app.grid[workingWall[0]-1][workingWall[1]] = 1
                                if ([workingWall[0]-1, workingWall[1]] not in walls):
                                    walls.append([workingWall[0]-1, workingWall[1]])
                        # Delete wall
                        for wall in walls:
                            if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                                walls.remove(wall)
                        continue

                # Delete the wall from the list anyway
                for wall in walls:
                    if (wall[0] == workingWall[0] and wall[1] == workingWall[1]):
                        walls.remove(wall)
                
            # Mark the remaining unvisited cells as walls
            for i in range(0, app.gridSize):
                for j in range(0, app.gridSize):
                    if (app.grid[i][j] == 'empty'):
                        app.grid[i][j] = 1
                        
            ####################################################################################################################################################
            #setup start and endpoints
            app.grid[startingRow][startingCol] = 2
            endingRow, endingCol = startingRow, startingCol
            while (endingRow, endingCol) == (startingRow, startingCol):
                tempEndingRow, tempEndingCol = random.randint(0, app.gridSize-1), random.randint(0, app.gridSize-1)
                if ((tempEndingCol-startingCol)**2 + (tempEndingRow-startingRow)**2)**0.5 > gridSize//2:
                    if app.grid[tempEndingRow][tempEndingCol] == 0:
                        endingRow, endingCol = tempEndingRow, tempEndingCol
            app.grid[endingRow][endingCol] = 3
            ####################################################################################################################################################
            pass
        
grid = level_gen(5)
print(grid.grid)
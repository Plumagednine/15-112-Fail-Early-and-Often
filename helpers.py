import ast
import decimal
from operator import indexOf
from cmu_112_graphics import *
import random
import math
import json
    
#######################################
###Helper Functions####################
#######################################

#######################################
###Math Functions######################
#######################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#######################################
###Grid Functions######################
#######################################
def distance(x0, y0, x1, y1):
    return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

def getCell(x, y, width, height, gridSize, xOffset = 0, yOffset = 0):
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    row =  (y-yOffset)//cellHeight
    col = (x-xOffset)//cellWidth
    return (row, col)

def getCellBounds(row, col, width, height, gridSize):
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    x0 = col * cellWidth
    y0 = row * cellHeight
    x1 = (col+1) * cellWidth
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

#######################################
###Graphics Functions##################
#######################################

def create_elipse(canvas, cx, cy, radius, **options):
    canvas.create_oval(cx - radius
                    , cy - radius
                    , cx + radius
                    , cy + radius
                    , **options)

def resizeSprite(sprite, width, height):
    sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
    return sprite

def updateSpriteDimensions(app, sprites, width, height, gridSize):
    for i in range(4):
        sprites[i] = resizeSprite(sprites[i], width//gridSize, height//gridSize)
    return sprites

def animateSprite(app, tokenPath, width, height, gridSize):
    spritestrip = app.loadImage(tokenPath)
    sprites = []
    for i in range(4):
        sprite = spritestrip.crop(((spritestrip.size[0]//4)*i, 0, (spritestrip.size[0]//4)+(spritestrip.size[0]//4)*i, spritestrip.size[1]))
        sprite = resizeSprite(sprite, width//gridSize, height//gridSize)
        sprites.append(sprite)   
    return sprites 

def updateItemDimensions(app, player, width, height, gridSize):
    for weapon in player.weapons:
        if weapon != 0:
            itemImage = resizeSprite(weapon.getItemImage(), width//gridSize-20, height//gridSize-20)
            weapon.setItemImage(itemImage)
    
#######################################
###File Management Functions###########
#######################################
    
def loadJSON(filePath):
    with open(filePath) as f:
        return json.load(f)
    
def loadText(filePath):
    with open(filePath) as f:
        return ast.literal_eval(f.read())
    
#######################################
###Debug Functions#####################
#######################################

def print2dList(list):
    for row in list:
        print(row)
        
#######################################
###Algorithms##########################
#######################################
# #####################################
###Line of Sight Algorithm############
#######################################
    # """
    # If the rise is greater than the run, then we iterate over the y values and adjust the x values as
    # needed. If the run is greater than the rise, then we iterate over the x values and adjust the y
    # values as needed
    
    # :param startPoint: (x,y) coordinates of the starting point
    # :param endPoint: The point you want to check if you can see
    # :param grid: a 2D array of 0s and 1s, where 0s are empty spaces and 1s are obstacles
    # :return: A boolean value.
    
    # Sources:
    # - [Bresenham's line algorithm Wikipedia](https://en.wikipedia.org/wiki/Bresenham's_line_algorithm)
    # - [Bresenham's line algorithm Geeks For Geeks](https://www.geeksforgeeks.org/bresenhams-line-generation-algorithm/)
    # - [Bresenham's line algorithm YouTube](https://www.youtube.com/watch?v=lKVo6oLsCXs&t=39s)
    # """
def lineOfSight(startPoint,endPoint,grid):
    x0, y0 = startPoint
    x1, y1 = endPoint
    rise = y1 - y0
    run = x1 - x0
    if run == 0:
        y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            if grid[y][x0] == 1:
                return False
    else:
        #run greater than rise
        slope = rise / run
        adjust = 1 if slope > 0 else -1
        offset = 0
        threshold = 0.5
        if slope <= 1 and slope >= -1:
            slope = abs(slope)
            y = y0
            if x1 < x0:
                x0, x1 = x1, x0
                y = y1
            for x in range(x0, x1 + 1):
                if grid[x][y] == 1:
                    return False
                offset += slope
                if offset >= threshold:
                    y += adjust
                    threshold += 1
        else:
            #run less than rise
            slope = abs(run/rise)
            x = x0
            if y1 < y0:
                y0, y1 = y1, y0
                x = x1
            for y in range(y0, y1 + 1):
                if grid[x][y] == 1:
                    return False
                offset += slope
                if offset >= threshold:
                    x += adjust
                    threshold += 1
    return True
#######################################
###A* Algorithm########################
#######################################
    # """
    # The function takes in a start point, end point and a grid. It then creates a start node and an end
    # node. It then creates an open list and a closed list. It then adds the start node to the open list.
    # It then loops through the open list and checks if the current node is the end node. If it is not
    # then it updates the open list. If it is then it returns the path.
    
    # :param row: the row of the starting point
    # :param col: the column of the starting point
    # :param grid: a 2D list of integers, where 0 is a walkable space, and 1 is a wall
    # :return: The path from the start to the end
    
    # Sources:
    # - [A* Search Algorithm Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
    # - [A* Search Algorithm Geeks For Geeks](https://www.geeksforgeeks.org/a-search-algorithm/)
    # - [A* Search Algorithm YouTube](https://www.youtube.com/watch?v=i0x5fj4PqP4)
    # """
#Create a node class
#Easier to work with than a dictionary or list
class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.position = pos

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

#chech if the move is valid:
def isValidMove(row, col, grid):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    if grid[row][col] == 1:
        return False
    return True

#update the open list
#main part of the A* algorithm            
def updateOpenList(currentPoint, openList, closedList, startPoint, endPoint, grid):
    possibleMoves = []
    #create a list of possible moves
    #also called children nodes
    for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        pointPos = (currentPoint.position[0] + newPos[0], currentPoint.position[1] + newPos[1])
        
        #check if the move is valid
        if not isValidMove(pointPos[0], pointPos[1], grid):
            continue
        
        #branch from the parent node
        newPoint = Node(currentPoint, pointPos)
        possibleMoves.append(newPoint)
    
    #Check all possible moves to see if they have been visited if they havent then add them to the open list
    for move in possibleMoves:
        for closed in closedList:
            if move == closed:
                continue
        
        #calculate the g, h and f values fir the child node
        move.g = currentPoint.g + 1
        move.h = abs(move.position[0] - endPoint.position[0]) + abs(move.position[1] - endPoint.position[1])
        move.f = move.g + move.h
        
        # add the child node to the open list if it is not already in the open list and is more optimal than the current node
        for open in openList:
            if move == open:
                if move.g > open.g:
                    continue
                
        openList.append(move)
        
    return openList

def returnPath(currentPoint, startPoint):
    path = []
    current = currentPoint
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]

def aStar(start, end, grid):
    startPoint = Node(None, start)
    startPoint.g = startPoint.h = startPoint.f = 0
    endPoint = Node(None, end)
    endPoint.g = endPoint.h = endPoint.f = 0
    
    openList = []
    closedList = []
    
    openList.append(startPoint)
    
    while openList:
        #get current node
        currentPoint = openList[0]
        currentIndex = 0
        
        #check if current node is more efficient
        for index in range(len(openList)):
            item = openList[index]
            if item.f < currentPoint.f:
                currentPoint = item
                currentIndex = index
        
        # remove current node from open list
        openList.pop(currentIndex)
        # add current node to closed list
        closedList.append(currentPoint)
        
        #check if current node is the end node otherwise loop again
        if currentPoint == endPoint:
            return returnPath(currentPoint, startPoint)
        else:
            openList = updateOpenList(currentPoint, openList, closedList, startPoint, endPoint, grid)



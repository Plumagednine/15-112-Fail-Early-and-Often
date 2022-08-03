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

def isValidMove(row, col, grid):
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    if grid[row][col] == 1:
        return False
    return True

def isNotWall(row, col, grid):
    return grid[row][col] != 1

class Node():
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.position = pos

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
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
        for index, item in enumerate(openList):
            if item.f < currentPoint.f:
                currentPoint = item
                currentIndex = index
        
        # remove current node from open list
        openList.pop(currentIndex)
        # add current node to closed list
        closedList.append(currentPoint)
        
        if currentPoint == endPoint:
            path = []
            current = currentPoint
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        # get next possible moves of current node
        possibleMoves = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            pointPos = (currentPoint.position[0] + newPos[0], currentPoint.position[1] + newPos[1])
            if not isValidMove(pointPos[0], pointPos[1], grid):
                continue
            if not isNotWall(pointPos[0], pointPos[1], grid):
                continue
            
            newPoint = Node(currentPoint, pointPos)
            possibleMoves.append(newPoint)
        
        for move in possibleMoves:
            for closed in closedList:
                if move == closed:
                    continue
            
            move.g = currentPoint.g + 1
            move.h = abs(move.position[0] - endPoint.position[0]) + abs(move.position[1] - endPoint.position[1])
            move.f = move.g + move.h
            
            for open in openList:
                if move == open:
                    if move.g > open.g:
                        continue
            
            openList.append(move)
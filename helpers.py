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
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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
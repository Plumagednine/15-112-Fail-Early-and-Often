import decimal
from cmu_112_graphics import *
import random
    
#######################################
###Helper Functions####################
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

def create_elipse(canvas, cx, cy, radius, **options):
    canvas.create_oval(cx - radius
                    , cy - radius
                    , cx + radius
                    , cy + radius
                    , **options)

def getCell(x, y, width, height, gridSize):
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    row =  y//cellHeight
    col = x//cellWidth
    return (row, col)

def getCellBounds(row, col, width, height, gridSize):
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    x0 = col * cellWidth
    y0 = row * cellHeight
    x1 = (col+1) * cellWidth
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

def resizeSprite(sprite, width, height):
    sprite = sprite.resize((width, height), Image.NEAREST)
    return sprite

def updateSpriteDimensions(app, sprites, width, height, gridSize):
    for i in range(4):
        sprites[i] = resizeSprite(sprites[i], width//gridSize, height//gridSize)
    return sprites

def animateSprite(app, tokenPath, width, height, gridSize):
    spritestrip = app.loadImage(tokenPath)
    sprites = []
    for i in range(4):
        sprite = spritestrip.crop((960*i, 0, 960+960*i, 960))
        sprite = resizeSprite(sprite, width//gridSize, height//gridSize)
        sprites.append(sprite)   
    return sprites 
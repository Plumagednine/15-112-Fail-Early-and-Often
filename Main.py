import os
from asyncio.locks import _ContextManagerMixin
from tkinter import *

from cmu_112_graphics import *
from level_generation import *
from Player import *
import math


#######################################
###Helper Functions####################
#######################################

def create_elipse(canvas, cx, cy, radius, **options):
    canvas.create_oval(cx - radius
                    , cy - radius
                    , cx + radius
                    , cy + radius
                    , **options)

def getCell(app, x, y, width, height, grid):
    (gridSize) = grid.getSize()
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    row =  y//cellHeight
    col = x//cellWidth
    return (row, col)

def getCellBounds(app, row, col, width, height, gridSize):
    cellWidth = width // gridSize
    cellHeight = height // gridSize
    x0 = col * cellWidth
    y0 = row * cellHeight
    x1 = (col+1) * cellWidth
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)


#######################################
###GUI Functions#######################
#######################################

def generateDungeon(app, canvas, grid):
    gridSize = grid.getSize()
    gridLayout = grid.getLayout()
    for row in range(gridSize):
        for col in range(gridSize):
            (x0, y0, x1, y1) = getCellBounds(app, row, col, app.gridWidth, app.gridHeight, gridSize)
            if gridLayout[row][col] == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#ffffff', width = 1)
            elif gridLayout[row][col] == 1:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#000000', width = 1)
            elif gridLayout[row][col] == 2:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#0000ff', width = 1)
            elif gridLayout[row][col] == 3:
                canvas.create_rectangle(x0, y0, x1, y1, fill='#00ff00', width = 1)
    pass

def drawPlayer(app, canvas, player):
    (x, y) = player.getPos()
    (x0, y0, x1, y1) = getCellBounds(app, x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
    canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, pilImage = player.getImage())
    pass

def redrawAll(app, canvas): # draw (view) the model in the canvas
    #Draw Background
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#000000')
    
    #start menu
    if app.startMenu:
        pass
    
    #win menu
    if app.winMenu:
        canvas.create_text(app.width//2, app.height//2, text="You Win!", fill='#ffffff', font='Arial 30')
        pass

#######################################
###While Game is Running###############
#######################################
    #Draw Game
    if (not app.startMenu and not app.winMenu):
        generateDungeon(app, canvas, app.dungeon)
        drawPlayer(app, canvas, app.player)
    pass      


#######################################
###Init Functions######################
#######################################
def resizeSprite(sprite, width, height):
    sprite = sprite.resize((width, height), Image.NEAREST)
    return sprite

def initPlayer(app, row, col, tokenPath):
    app.playerSprite = app.loadImage(tokenPath)
    app.playerSprite = resizeSprite(app.playerSprite, app.gridWidth//app.dungeon.getSize(), app.gridHeight//app.dungeon.getSize())
    app.player = Player(row, col, app.playerSprite)

def initDungeon(app, gridSize): 
    app.dungeon = level_generation(gridSize)

def initSidebar(app, canvas):
    pass

def initDimensions(app):
    app.gridWidth = app.width-int(app.height*.5)
    app.gridHeight = app.height
    app.sidebarWidth = app.width-app.gridWidth
    app.sidebarHeight = app.height
    pass

def updateSpriteDimensions(app):
        app.playerSprite  = resizeSprite(app.playerSprite, app.gridWidth//app.dungeon.getSize(), app.gridHeight//app.dungeon.getSize())
        app.player.updateSprite(app.playerSprite)

def appStarted(app): # initialize the model (app.xyz)
#######################################
###Make System Variables###############
#######################################
    app.framerate = 30
    app.timerDelay = 1000//app.framerate
    app.startMenu = False
    app.winMenu = False
    initDimensions(app)
#######################################
###Make Dungeon and Player#############
#######################################
    initDungeon(app, 16)
    app.spawnPoint = app.dungeon.getSpawnPoint()
    app.endPoint = app.dungeon.getEndPoint()
    initPlayer(app, app.spawnPoint[0], app.spawnPoint[1], 'sprites\humanfigher1-1x1.gif')
    pass           

def appStopped(app): # cleanup after app is done running
    pass           



#######################################
###User Input##########################
#######################################

def keyPressed(app, event): # use event.key
    if (not app.startMenu and not app.winMenu):
        grid = app.dungeon.getLayout()
        playerPOS = app.player.getPos()
        if event.key == 'w' and app.player.getPos()[0] > 0:
            if grid[playerPOS[0]-1][playerPOS[1]] != 1:
                app.player.moveUp()
            pass
        elif event.key == 'a' and app.player.getPos()[1] > 0:
            if grid[playerPOS[0]][playerPOS[1]-1] != 1:
                app.player.moveLeft()
            pass
        elif event.key == 's' and app.player.getPos()[0] < app.dungeon.getSize()-1:
            if grid[playerPOS[0]+1][playerPOS[1]] != 1:
                app.player.moveDown()
            pass
        elif event.key == 'd' and (app.player.getPos()[1]) < app.dungeon.getSize()-1:
            if grid[playerPOS[0]][playerPOS[1]+1] != 1:
                app.player.moveRight()
            pass
        if app.player.getPos() == app.endPoint:
            print("You Win!")
            app.winMenu = True
            pass
        
    if app.startMenu:
        pass
    
    if app.winMenu:
        pass
        
    pass    

# def keyReleased(app, event): # use event.key
    # pass   

def mousePressed(app, event): # use event.x and event.y
    pass  

# def mouseReleased(app, event): # use event.x and event.y
#     pass 

# def mouseMoved(app, event): # use event.x and event.y
#     pass    

# def mouseDragged(app, event): # use event.x and event.y
#     pass  


#######################################
###System Changes#############
#######################################

def timerFired(app): # respond to timer events
    pass           

def sizeChanged(app): # respond to window size changes
    initDimensions(app)
    updateSpriteDimensions(app)
    pass  

            
runApp(width = 1200, height = 800, title = '15-112: Fail Early and Often')
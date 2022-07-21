import os
from asyncio.locks import _ContextManagerMixin
from tkinter import *
import pyglet

from cmu_112_graphics import *
from level_generation import *
from Player import *
import math


#######################################
###Helper Functions####################
#######################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
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

def getCell(app, x, y, width, height, gridSize):
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


#######################################
###Game Draw Functions#################
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

def drawSidebar(app, canvas):
    canvas.create_text(app.sidebarMinWidth, app.sidebarMinHeight, text="Player Stats and Inventory:", fill='#ffffff', font=(app.font,14), anchor = 'nw')
    # create health bar
    healthBarMultiplier = app.player.getHealthMultiplyer()
    healthBarSize = (app.sidebarMaxWidth - app.sidebarMinWidth) * healthBarMultiplier
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMaxWidth, app.sidebarMaxHeight//10+20, fill='#ff0000')
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMinWidth + healthBarSize, app.sidebarMaxHeight//10+20, fill='#00ff00')
    canvas.create_text(app.sidebarMinWidth+10, (app.sidebarMinHeight+app.sidebarMaxHeight//10)//2+20
                       , text=f'Health: {app.player.getHealth()}', fill='#ffffff', font=(app.font,14), anchor = 'w')
    pass


#######################################
###Start Menu Draw Functions###########
#######################################
def drawStartMenu(app, canvas):
    #make interactive grid
    gridSize = 10
    startButton = []
    title = []
    for row in range(gridSize):
        for col in range(gridSize):
            (x0, y0, x1, y1) = getCellBounds(app, row, col, app.width, app.height, gridSize)
            canvas.create_rectangle(x0, y0, x1, y1, fill='#ffffff', width = 0)
            if app.startMenuGrid[row][col] == 1: 
                title.append((row,col))
            if app.startMenuGrid[row][col] == 2:
                startButton.append((row,col))
    
    #make background image
    canvas.create_image(app.width//2,0,anchor = 'n', pilImage = app.startMenuBackground)
    
    # make title
    midIndex = len(title)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app, title[midIndex][0], title[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="15-112: Fail Early and Often", fill='#000000', font=(app.font,60), anchor = 'n',)
    
    # make start button
    midIndex = len(startButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app, startButton[midIndex][0], startButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Start Game", fill='#000000', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Redraw All##########################
#######################################
def redrawAll(app, canvas): # draw (view) the model in the canvas
    #Draw Background
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#000000')
    
    #start menu
    if app.gameState == 'start':
        drawStartMenu(app, canvas)
        pass
    
    #win menu
    if app.gameState == 'win':
        canvas.create_text(app.width//2, app.height//2, text="You Win!", fill='#ffffff', font=(app.font,25))
        pass

    #Draw Game
    if app.gameState == 'game':
        generateDungeon(app, canvas, app.dungeon)
        drawPlayer(app, canvas, app.player)
        drawSidebar(app, canvas)
    pass      

#######################################
###Init Functions######################
#######################################


#######################################
###Game Initializers###################
#######################################
def resizeSprite(sprite, width, height):
    sprite = sprite.resize((width, height), Image.NEAREST)
    return sprite

def initPlayer(app, row, col, tokenPath, hitPoints = 100, strength = 10
               , dexterity = 10, constitution = 10, movementSpeed = 30):
    app.playerSprite = app.loadImage(tokenPath)
    app.playerSprite = resizeSprite(app.playerSprite, app.gridWidth//app.dungeon.getSize(), app.gridHeight//app.dungeon.getSize())
    app.player = Player(row, col, app.playerSprite, hitPoints, strength, dexterity, constitution, movementSpeed)

def initDungeon(app, gridSize): 
    app.dungeon = level_generation(gridSize)

def initSidebar(app):
    cellWidth = app.sidebarWidth // app.dungeon.getSize()
    cellHeight = app.sidebarHeight // app.dungeon.getSize()
    app.sidebarMinWidth = app.gridWidth + app.gridWidth//app.dungeon.getSize()
    app.sidebarMinHeight = app.gridHeight//app.dungeon.getSize()
    app.sidebarMaxWidth = app.width - app.gridWidth//app.dungeon.getSize()
    app.sidebarMaxHeight = app.height - app.gridHeight//app.dungeon.getSize()
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

#######################################
###Start Menu Initializers#############
#######################################
        
def initStartMenu(app):
    # create a 10x10 grid
    gridSize = 10
    app.startMenuGrid = []
    gridRow = []
    app.startGameButton = [(2,3),(2,4),(2,5),(2,6)]
    titleCard = [(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
    for row in range(gridSize):
        for col in range(gridSize):
            gridRow.append(0)
        app.startMenuGrid.append(gridRow)
        gridRow=[]
        
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in titleCard:
                app.startMenuGrid[row][col] = 1
            elif (row,col) in app.startGameButton:
                app.startMenuGrid[row][col] = 2
                
    # make image
    smallerSide = min(app.width, app.height)
    imgDimensions = int(smallerSide*0.73), smallerSide
    app.startMenuBackground = app.loadImage('textures\TitleCard.png')
    app.startMenuBackground = resizeSprite(app.startMenuBackground, imgDimensions[0], imgDimensions[1])
    pass

#######################################
###App First Run#######################
#######################################
def appStarted(app): # initialize the model (app.xyz)
    #Make System Variables
    app.framerate = 30
    app.timerDelay = 1000//app.framerate
    app.gameState = 'start'
    pyglet.font.add_file('font\Vecna-oppx.ttf')
    app.font = 'Vecna-oppx'
    initDimensions(app)
    
    #make start Menu
    initStartMenu(app)
    
    #Make Dungeon and Player
    initDungeon(app, 16)
    app.spawnPoint = app.dungeon.getSpawnPoint()
    app.endPoint = app.dungeon.getEndPoint()
    initPlayer(app, app.spawnPoint[0], app.spawnPoint[1], 'sprites\humanfigher1-1x1.gif')
    initSidebar(app)
    pass           

def appStopped(app): # cleanup after app is done running
    pass           

#######################################
###User Input##########################
#######################################

def keyPressed(app, event): # use event.key
    if app.gameState == 'game':
        grid = app.dungeon.getLayout()
        playerPOS = app.player.getPos()
        #movement
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
            app.gameState = 'win'
            pass
        #attack
        if event.key == 'e':
            app.player.takeDamage(10)
            pass
        
    if app.gameState == 'start':
        pass
    
    if app.gameState == 'win':
        pass
        
    pass    

# def keyReleased(app, event): # use event.key
    # pass   

def mousePressed(app, event): # use event.x and event.y
    (row,col) = getCell(app, event.x, event.y, app.width, app.height, 10)
    if app.gameState == 'start':
        if (row,col) in app.startGameButton:
            app.gameState = 'game'
            pass
        pass
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
    initSidebar(app)
    initStartMenu(app)
    pass  

            
runApp(width = 1200, height = 800, title = '15-112: Fail Early and Often')
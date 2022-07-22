from tkinter import *
import pyglet

from cmu_112_graphics import *
from helpers import *
from level_generation import *
from Player import *
from Items import *
from loadData import *


#######################################
###GUI Functions#######################
#######################################


#######################################
###Game Draw Functions#################
#######################################
def drawSidebar(app, canvas):
    canvas.create_text(app.sidebarMinWidth, app.sidebarMinHeight, text="Player Stats and Inventory:", fill='#fffcf9', font=(app.font,14), anchor = 'nw')
    # create health bar
    healthBarMultiplier = app.playerCharacter.getHealthMultiplyer()
    healthBarSize = (app.sidebarMaxWidth - app.sidebarMinWidth) * healthBarMultiplier
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMaxWidth, app.sidebarMaxHeight//10+20, fill='#f71735')
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMinWidth + healthBarSize, app.sidebarMaxHeight//10+20, fill='#44af69')
    canvas.create_text(app.sidebarMinWidth+10, (app.sidebarMinHeight+app.sidebarMaxHeight//10)//2+20
                       , text=f'Health: {app.playerCharacter.getHealth()}', fill='#fffcf9', font=(app.font,14), anchor = 'w')
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
            (x0, y0, x1, y1) = getCellBounds(row, col, app.width, app.height, gridSize)
            canvas.create_rectangle(x0, y0, x1, y1, fill='#fffcf9', width = 0)
            if app.startMenuGrid[row][col] == 1: 
                title.append((row,col))
            if app.startMenuGrid[row][col] == 2:
                startButton.append((row,col))
    
    #make background image
    canvas.create_image(app.width//2,0,anchor = 'n', pilImage = app.startMenuBackground)
    
    # make title
    midIndex = len(title)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(title[midIndex][0], title[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="15-112: Fail Early and Often", fill='#1c0f13', font=(app.font,60), anchor = 'n',)
    
    # make start button
    midIndex = len(startButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(startButton[midIndex][0], startButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Start Game", fill='#1c0f13', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Redraw All##########################
#######################################
def redrawAll(app, canvas): # draw (view) the model in the canvas
    #Draw Background
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#1c0f13')
    
    #start menu
    if app.gameState == 'start':
        drawStartMenu(app, canvas)
        pass
    
    #win menu
    if app.gameState == 'win':
        canvas.create_text(app.width//2, app.height//2, text="You Win!", fill='#fffcf9', font=(app.font,25))
        pass

    #Draw Game
    if app.gameState == 'game':
        app.dungeon.drawDungeon(app, canvas)
        app.playerCharacter.drawPlayer(app, canvas)
        drawSidebar(app, canvas)
    pass      

#######################################
###Init Functions######################
#######################################


#######################################
###Game Initializers###################
#######################################

def initPlayer(app, player):
    spriteSheet = player.sprites
    app.playerCharacterSprites = animateSprite(app, spriteSheet, app.gridWidth, app.gridHeight, app.dungeon.getSize()) 
    player.sprites = app.playerCharacterSprites
    player.row, player.col = app.dungeon.getSpawnPoint()
    pass

def initDungeon(app, gridSize): 
    app.dungeon = level_generation(gridSize)
    pass

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
    app.animationTimer = 0
    app.gameState = 'start'
    allCharacters = loadPlayerCharacters()
    app.playerCharacter = allCharacters.get('Default Character')
    pyglet.font.add_file('font\Vecna-oppx.ttf')
    app.font = 'Vecna-oppx'
    initDimensions(app)
    
    #make start Menu
    initStartMenu(app)
    
    #Make Dungeon and Player
    initDungeon(app, 16)
    app.spawnPoint = app.dungeon.getSpawnPoint()
    app.endPoint = app.dungeon.getEndPoint()
    initPlayer(app, app.playerCharacter)
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
        playerPOS = app.playerCharacter.getPos()
        #movement
        if event.key == 'w' and app.playerCharacter.getPos()[0] > 0:
            if grid[playerPOS[0]-1][playerPOS[1]] != 1:
                app.playerCharacter.moveUp()

        elif event.key == 'a' and app.playerCharacter.getPos()[1] > 0:
            if grid[playerPOS[0]][playerPOS[1]-1] != 1:
                app.playerCharacter.moveLeft()

        elif event.key == 's' and app.playerCharacter.getPos()[0] < app.dungeon.getSize()-1:
            if grid[playerPOS[0]+1][playerPOS[1]] != 1:
                app.playerCharacter.moveDown()

        elif event.key == 'd' and (app.playerCharacter.getPos()[1]) < app.dungeon.getSize()-1:
            if grid[playerPOS[0]][playerPOS[1]+1] != 1:
                app.playerCharacter.moveRight()

        if app.playerCharacter.getPos() == app.endPoint:
            app.gameState = 'win'
        
    if app.gameState == 'start':
        pass
    
    if app.gameState == 'win':
        pass
        
    pass    

# def keyReleased(app, event): # use event.key
    # pass   

def mousePressed(app, event): # use event.x and event.y
    (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
    if app.gameState == 'start':
        if (row,col) in app.startGameButton:
            app.gameState = 'game'
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
    app.animationTimer += app.framerate
    if app.animationTimer >= 100:
        app.animationTimer = 0
        app.playerCharacter.animateSprite(app)
    pass           

def sizeChanged(app): # respond to window size changes
    initDimensions(app)
    app.playerCharacter.updateSprite(updateSpriteDimensions(app, app.playerCharacter.getSprites(), app.gridWidth, app.gridHeight, app.dungeon.getSize()))
    initSidebar(app)
    initStartMenu(app)
    pass  

            
runApp(width = 1200, height = 800, title = '15-112: Fail Early and Often')
from tkinter import *
import pyglet

from cmu_112_graphics import *
from helpers import *
from Dungeon import *
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
    # """
    # It draws the sidebar.

    # :param app: the app object
    # :param canvas: the canvas to draw on
    # """
    canvas.create_text(app.sidebarMinWidth, app.sidebarMinHeight, text="Player Stats and Inventory:", fill='#fffcf9', font=(app.font,14), anchor = 'nw')
    # create health bar
    healthBarMultiplier = app.playerCharacter.getHealthMultiplyer()
    healthBarSize = (app.sidebarMaxWidth - app.sidebarMinWidth) * healthBarMultiplier
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMaxWidth, app.sidebarMaxHeight//10+20, fill='#f71735')
    canvas.create_rectangle(app.sidebarMinWidth, app.sidebarMinHeight+20, app.sidebarMinWidth + healthBarSize, app.sidebarMaxHeight//10+20, fill='#44af69')
    canvas.create_text(app.sidebarMinWidth+10, (app.sidebarMinHeight+app.sidebarMaxHeight//10)//2+20
                    , text=f'Health: {app.playerCharacter.getHealth():.0f}', fill='#fffcf9', font=(app.font,14), anchor = 'w')
    
    #create weapon inventory
    for col in range(len(app.playerCharacter.weapons)):
        (x0, y0, x1, y1) = getCellBounds(0, col, app.sidebarActualWidth, app.sidebarActualWidth, len(app.playerCharacter.weapons))
        if col == app.playerCharacter.currentWeapon:
            canvas.create_rectangle(x0+app.sidebarMinWidth, y0+app.sidebarMaxHeight//10+40,
                                x1+app.sidebarMinWidth, y1+app.sidebarMaxHeight//10+40, fill='#F686BD', width = 1)
        canvas.create_rectangle(x0+app.sidebarMinWidth+10, y0+app.sidebarMaxHeight//10+40+10,
                                x1+app.sidebarMinWidth-10, y1+app.sidebarMaxHeight//10+40-10, fill='#fffcf9', width = 1)
        if app.playerCharacter.weapons[col] != 0:
            canvas.create_image(x0 + (x1-x0)//2 + app.sidebarMinWidth, y0 + (y1-y0)//2 +app.sidebarMaxHeight//10+40,
                                image=ImageTk.PhotoImage(app.playerCharacter.weapons[col].itemImage))
    
    #create armor inventory
    for col in range(len(app.playerCharacter.armor)):
        (x0, y0, x1, y1) = getCellBounds(1, col, app.sidebarActualWidth, app.sidebarActualWidth, len(app.playerCharacter.armor))
        if col == app.playerCharacter.currentArmor:
            canvas.create_rectangle(x0+app.sidebarMinWidth, y0+app.sidebarMaxHeight//10+40,
                                x1+app.sidebarMinWidth, y1+app.sidebarMaxHeight//10+40, fill='#F686BD', width = 1)
        canvas.create_rectangle(x0+app.sidebarMinWidth+10, y0+app.sidebarMaxHeight//10+40+10,
                                x1+app.sidebarMinWidth-10, y1+app.sidebarMaxHeight//10+40-10, fill='#fffcf9', width = 1)
        if app.playerCharacter.armor[col] != 0:
            canvas.create_image(x0 + (x1-x0)//2 + app.sidebarMinWidth, y0 + (y1-y0)//2 +app.sidebarMaxHeight//10+40,
                                image=ImageTk.PhotoImage(app.playerCharacter.armor[col].itemImage))
    
    #create misc item inventory
    for col in range(len(app.playerCharacter.miscItems)):
        (x0, y0, x1, y1) = getCellBounds(2, col, app.sidebarActualWidth, app.sidebarActualWidth, len(app.playerCharacter.miscItems))
        if col == app.playerCharacter.currentItem:
            canvas.create_rectangle(x0+app.sidebarMinWidth, y0+app.sidebarMaxHeight//10+40,
                                x1+app.sidebarMinWidth, y1+app.sidebarMaxHeight//10+40, fill='#F686BD', width = 1)
        canvas.create_rectangle(x0+app.sidebarMinWidth+10, y0+app.sidebarMaxHeight//10+40+10,
                                x1+app.sidebarMinWidth-10, y1+app.sidebarMaxHeight//10+40-10, fill='#fffcf9', width = 1)
        if app.playerCharacter.miscItems[col] != 0:
            canvas.create_image(x0 + (x1-x0)//2 + app.sidebarMinWidth, y0 + (y1-y0)//2 +app.sidebarMaxHeight//10+40,
                                image=ImageTk.PhotoImage(app.playerCharacter.miscItems[col].itemImage))      
    pass


#######################################
###Start Menu Draw Functions###########
#######################################
def drawStartMenu(app, canvas):
    # """
    # This function draws the start menu of the game
    
    # :param app: the app object
    # :param canvas: the canvas that you're drawing on
    # """
    #make interactive grid
    gridSize = 10
    startButton = []
    title = []
    characterSelect = []
    for row in range(gridSize):
        for col in range(gridSize):
            (x0, y0, x1, y1) = getCellBounds(row, col, app.width, app.height, gridSize)
            canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 0)
            if app.startMenuGrid[row][col] == 1: 
                title.append((row,col))
            if app.startMenuGrid[row][col] == 2:
                startButton.append((row,col))
            if app.startMenuGrid[row][col] == 3:
                characterSelect.append((row,col))
    
    #make background image
    # canvas.create_image(app.width//2,0,anchor = 'n', pilImage = app.startMenuBackground)
    
    # make title
    midIndex = len(title)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(title[midIndex][0], title[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="15-112: Fail Early and Often", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make start button
    midIndex = len(startButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(startButton[midIndex][0], startButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Start Game", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    
    # make characterSelect button
    midIndex = len(startButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(characterSelect[midIndex][0], characterSelect[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Select Character", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Pause Menu Draw Functions###########
#######################################
def drawPauseMenu(app, canvas):
    #make interactive grid
    gridSize = 10
    # make continue button
    midIndex = len(app.contineuGameButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.contineuGameButton[midIndex][0], app.contineuGameButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Continue Game", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make exit button
    midIndex = len(app.exitToStartButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.exitToStartButton[midIndex][0], app.exitToStartButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Exit To Start Menu", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Continue Menu Draw Functions########
#######################################
def drawContinueMenu(app, canvas):
    #make interactive grid
    gridSize = 10
    
    # make continue button
    midIndex = len(app.levelCounter)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.levelCounter[midIndex][0], app.levelCounter[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text=f"Level: {app.currentLevel-1} Completed", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make continue button
    midIndex = len(app.contineuGameButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.contineuGameButton[midIndex][0], app.contineuGameButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Continue Game", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make exit button
    midIndex = len(app.exitToStartButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.exitToStartButton[midIndex][0], app.exitToStartButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Exit To Start Menu", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Death Screen Draw Functions#########
#######################################
def drawDeathScreen(app, canvas):
    #make interactive grid
    gridSize = 10
    
    # make continue button
    midIndex = len(app.levelCounter)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.levelCounter[midIndex][0], app.levelCounter[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text=f"You Made it to Level: {app.currentLevel}", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make death text button
    midIndex = len(app.youDiedText)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.youDiedText[midIndex][0], app.youDiedText[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="You Died", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make exit button
    midIndex = len(app.exitToStartButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.exitToStartButton[midIndex][0], app.exitToStartButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Exit To Start Menu", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    pass

#######################################
###Loading Screen Draw Functions#######
#######################################
def drawLoadingScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill='#1c0f13', width = 0)
    canvas.create_text(app.width//2,app.height//2, text="Loading...", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    
    
#######################################
###Character Selection Draw Functions##
#######################################
                
def drawCharacterSelection(app, canvas):
    #make interactive grid
    gridSize = 10
    exitToStartButton = []
    changeCharacterButton = []
    characterText = []
    for row in range(gridSize):
        for col in range(gridSize):
            (x0, y0, x1, y1) = getCellBounds(row, col, app.width, app.height, gridSize)
            canvas.create_rectangle(x0, y0, x1, y1, fill='#1c0f13', width = 0)
            if app.charcterSelectionGrid[row][col] == 1: 
                exitToStartButton.append((row,col))
            if app.charcterSelectionGrid[row][col] == 2:
                characterText.append((row,col))
            if app.charcterSelectionGrid[row][col] == 3: 
                changeCharacterButton.append((row,col))
    
    # make current character text
    midIndex = len(characterText)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(characterText[midIndex][0], characterText[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text=f"Current Character: {app.currentCharacter}", fill='#fffcf9', font=(app.font,45), anchor = 'n',)
    
    # make start button
    midIndex = len(changeCharacterButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(changeCharacterButton[midIndex][0], changeCharacterButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Change Character", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    
    # make characterSelect button
    midIndex = len(exitToStartButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(exitToStartButton[midIndex][0], exitToStartButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Exit To Start Menu", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    # pass

#######################################
###Pause Menu Draw Functions###########
#######################################
def drawPauseMenu(app, canvas):
    #make interactive grid
    gridSize = 10
    # make continue button
    midIndex = len(app.contineuGameButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.contineuGameButton[midIndex][0], app.contineuGameButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Continue Game", fill='#fffcf9', font=(app.font,60), anchor = 'n',)
    
    # make exit button
    midIndex = len(app.exitToStartButton)//2
    tempX0,tempY0,tempX1,tempY1 = getCellBounds(app.exitToStartButton[midIndex][0], app.exitToStartButton[midIndex][1], app.width, app.height, gridSize)
    canvas.create_text(tempX0,tempY0, text="Exit To Start Menu", fill='#fffcf9', font=(app.font,60), anchor = 'n')
    
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
    if app.gameState == 'loadingScreen':
        drawLoadingScreen(app, canvas)
        pass

    #Draw Game
    if app.gameState == 'game':
        if app.map:
            app.dungeon.drawDungeon(app, canvas)
        else:
            app.currentRoom.drawRoom(app, canvas)
        app.playerCharacter.drawPlayer(app, canvas, app.map)
        drawSidebar(app, canvas)
        
    if app.gameState == 'pauseMenu':
        drawPauseMenu(app, canvas)
    
    if app.gameState == 'continueMenu':
        drawContinueMenu(app, canvas)
    
    if app.gameState == 'deathScreen':
        drawDeathScreen(app, canvas)
    
    if app.gameState == 'characterSelection':
        drawCharacterSelection(app, canvas)
    pass      

#######################################
###Init Functions######################
#######################################


#######################################
###Game Initializers###################
#######################################
def continueGame(app):
    app.currentLevel += 1
    initDungeon(app, app.allRooms, app.dungeonSize)
    dungeonRow,dungeonCol = app.spawnPointDungeon
    roomRow,roomCol = app.dungeon.getRoom(app.dungeon.getSpawnPoint()[0],app.dungeon.getSpawnPoint()[1]).getPlayerSpawn()
    app.playerCharacter.setDungeonPos(dungeonRow,dungeonCol)
    app.playerCharacter.setRoomPos(roomRow,roomCol)

def initPlayer(app, player):
    spriteSheet = player.sprites
    app.playerCharacterSprites = animateSprite(app, spriteSheet, app.gridWidth, app.gridHeight, app.dungeon.getSize()) 
    player.sprites = app.playerCharacterSprites
    player.dungeonRow, player.dungeonCol = app.dungeon.getSpawnPoint()
    player.roomRow, player.roomCol = app.dungeon.getRoom(app.dungeon.getSpawnPoint()[0],app.dungeon.getSpawnPoint()[1]).getPlayerSpawn()
    app.playerMaxMoves = player.movementSpeed
    app.playerMovesLeft = app.playerMaxMoves
    pass

def initMonster(app, monster):
    spriteSheet = monster.sprites
    app.monsterCharacterSprites = animateSprite(app, spriteSheet, app.gridWidth, app.gridHeight, app.dungeon.getSize()) 
    monster.sprites = app.monsterCharacterSprites
    monster.dungeonRow, monster.dungeonCol = app.dungeon.getSpawnPoint()
    pass

def initDungeon(app, allRooms, gridSize): 
    app.dungeon = level_generation(allRooms, gridSize)
    print2dList(app.dungeon.getLayout())
    app.spawnPointDungeon = app.dungeon.getSpawnPoint()
    app.endPointDungeon = app.dungeon.getEndPoint()
    app.currentRoom = app.dungeon.getRoom(app.spawnPointDungeon[0], app.spawnPointDungeon[1])
    pass

def initDimensions(app):
    app.gridWidth = app.width-int(app.height*.5)
    app.gridHeight = app.height
    app.sidebarWidth = app.width-app.gridWidth
    app.sidebarHeight = app.height
    app.sidebarMinWidth = app.gridWidth + app.gridWidth//app.dungeonSize
    app.sidebarMinHeight = app.gridHeight//app.dungeonSize
    app.sidebarMaxWidth = app.width - app.gridWidth//app.dungeonSize
    app.sidebarMaxHeight = app.height - app.gridHeight//app.dungeonSize
    app.sidebarActualWidth = app.sidebarMaxWidth - app.sidebarMinWidth
    app.sidebarActualHeight = app.sidebarMaxHeight - app.sidebarMinHeight
    pass

def initSidebar(app):
    #get inventory images
    weapons = app.playerCharacter.weapons
    for weapon in weapons:
        if weapon != 0:
            weaponImage = app.loadImage(weapon.itemImage)
            weaponImage = weaponImage.resize(((app.sidebarActualWidth)//len(weapons)-20, (app.sidebarActualWidth)//len(weapons)-20), Image.Resampling.LANCZOS)
            weapon.itemImage = weaponImage
    armors = app.playerCharacter.armor
    for armor in armors:
        if armor != 0:
            armorImage = app.loadImage(armor.itemImage)
            armorImage = armorImage.resize(((app.sidebarActualWidth)//len(armors)-20, (app.sidebarActualWidth)//len(armors)-20), Image.Resampling.LANCZOS)
            armor.itemImage = armorImage
    miscItems = app.playerCharacter.miscItems
    for item in miscItems:
        if item != 0:
            itemImage = app.loadImage(item.itemImage)
            itemImage = itemImage.resize(((app.sidebarActualWidth)//len(miscItems)-20, (app.sidebarActualWidth)//len(miscItems)-20), Image.Resampling.LANCZOS)
            item.itemImage = itemImage
    pass



#######################################
###Start Menu Initializers#############
#######################################
        
def initStartMenu(app):
    # create a 10x10 grid
    gridSize = 10
    app.startMenuGrid = [[0 for row in range(gridSize)] for col in range(gridSize)]
    gridRow = []
    app.startGameButton = [(2,3),(2,4),(2,5),(2,6)]
    titleCard = [(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
    app.characterSelectionButton = [(4,3),(4,4),(4,5),(4,6)]
    # for row in range(gridSize):
    #     for col in range(gridSize):
    #         gridRow.append(0)
    #     app.startMenuGrid.append(gridRow)
    #     gridRow=[]
        
    
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in titleCard:
                app.startMenuGrid[row][col] = 1
            elif (row,col) in app.startGameButton:
                app.startMenuGrid[row][col] = 2
            elif (row,col) in app.characterSelectionButton:
                app.startMenuGrid[row][col] = 3
                
    # make image
    smallerSide = min(app.width, app.height)
    imgDimensions = int(smallerSide*0.73), smallerSide
    app.startMenuBackground = app.loadImage('textures\TitleCard.png')
    app.startMenuBackground = resizeSprite(app.startMenuBackground, imgDimensions[0], imgDimensions[1])
    pass

#######################################
###Pause Menu Initializers#############
#######################################
        
def initPauseMenu(app):
    # create a 10x10 grid
    gridSize = 10
    app.pauseMenuGrid = []
    gridRow = []
    app.contineuGameButton = [(3,2),(3,3),(3,4),(3,5),(3,6),(3,7)]
    app.exitToStartButton = [(6,2),(6,3),(6,4),(6,5),(6,6),(6,7)]
    contineuGameButton = app.contineuGameButton
    exitToStartButton = app.exitToStartButton
    for row in range(gridSize):
        for col in range(gridSize):
            gridRow.append(0)
        app.pauseMenuGrid.append(gridRow)
        gridRow=[]
        
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in contineuGameButton:
                app.pauseMenuGrid[row][col] = 1
            elif (row,col) in exitToStartButton:
                app.pauseMenuGrid[row][col] = 2
                
#######################################
###Continue Menu Initializers##########
#######################################
        
def initContinueMenu(app):
    # create a 10x10 grid
    gridSize = 10
    app.pauseMenuGrid = []
    gridRow = []
    app.levelCounter = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)]
    app.contineuGameButton = [(4,2),(4,3),(4,4),(4,5),(4,6),(4,7)]
    app.exitToStartButton = [(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
    contineuGameButton = app.contineuGameButton
    exitToStartButton = app.exitToStartButton
    for row in range(gridSize):
        for col in range(gridSize):
            gridRow.append(0)
        app.pauseMenuGrid.append(gridRow)
        gridRow=[]
        
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in contineuGameButton:
                app.pauseMenuGrid[row][col] = 1
            elif (row,col) in exitToStartButton:
                app.pauseMenuGrid[row][col] = 2
                
#######################################
###Death Screen Initializers##########
#######################################
        
def initDeathScreen(app):
    # create a 10x10 grid
    gridSize = 10
    app.pauseMenuGrid = []
    gridRow = []
    app.youDiedText = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)]
    app.levelCounter = [(4,2),(4,3),(4,4),(4,5),(4,6),(4,7)]
    app.exitToStartButton = [(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
    exitToStartButton = app.exitToStartButton
    for row in range(gridSize):
        for col in range(gridSize):
            gridRow.append(0)
        app.pauseMenuGrid.append(gridRow)
        gridRow=[]
        
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in exitToStartButton:
                app.pauseMenuGrid[row][col] = 1
                
#######################################
###Character Selection Initializers####
#######################################
        
def initCharacterSelectionScreen(app):
    # create a 10x10 grid
    gridSize = 10
    app.charcterSelectionGrid = []
    gridRow = []
    characterText = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)]
    app.changeCharacterButton = [(3,2),(3,3),(3,4),(3,5),(3,6),(3,7)]
    app.exitToStartButton = [(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
    exitToStartButton = app.exitToStartButton
    for row in range(gridSize):
        for col in range(gridSize):
            gridRow.append(0)
        app.charcterSelectionGrid.append(gridRow)
        gridRow=[]
        
    # add buttons
    for row in range(gridSize):
        for col in range(gridSize):
            if (row,col) in exitToStartButton:
                app.charcterSelectionGrid[row][col] = 1
            if (row,col) in characterText:
                app.charcterSelectionGrid[row][col] = 2
            if (row,col) in app.changeCharacterButton:
                app.charcterSelectionGrid[row][col] = 3
            
                
#######################################
###App First Run#######################
#######################################
def appStarted(app, character = 'Default Character'): # initialize the model (app.xyz)
    #Make System Variables
    app.framerate = 30
    app.timerDelay = 1000//app.framerate
    app.animationTimer = 0
    
    app.dungeonSize = 16
    app.gameState = 'start'
    app.turn = 'player'
    app.currentLevel = 1
    app.currentCharacter = character
    app.map = False
    app.roomImages = False
    
    #font stuff
    pyglet.font.add_file('font\Vecna-oppx.ttf')
    app.font = 'Vecna-oppx'
        
    #GUI Dimensions
    initDimensions(app)
    
    # #make monster
    app.allMonsters = loadMonsters()
    # app.testMonster = allMonsters.get('Default Monster')
    # initMonster(app, app.testMonster)
    
    #make items
    app.allItems = loadItems()
    
    #make rooms
    app.allRooms = loadRooms(app, app.allItems, app.allMonsters)

    #Make Dungeon
    initDungeon(app, app.allRooms, app.dungeonSize)
    
    #Make Start Menu
    initStartMenu(app)
    initCharacterSelectionScreen(app)
    
    #Make Player
    app.allCharacters = loadPlayerCharacters(app.allItems)
    app.playerCharacter = app.allCharacters.get(app.currentCharacter)
    initPlayer(app, app.playerCharacter)
    
    #make sidebar
    initSidebar(app)
    
    #make pause menu
    initPauseMenu(app)  
    
    #make continue menu
    initContinueMenu(app)  
    
    #make death screen menu
    initDeathScreen(app)  

def appStopped(app): # cleanup after app is done running
    pass           

#######################################
###User Input##########################
#######################################

def keyPressed(app, event): # use event.key
    #debug keypresses
    if event.key == "control-1":
        app.roomImages = not app.roomImages
    if event.key == "control-2":
        app.map = not app.map
    if event.key == "control-3":
        appStarted(app)
    
        
    if app.gameState == 'pauseMenu':
        if event.key == 'Escape':
            app.gameState = 'game'
    
    elif app.gameState == 'game':
        grid = app.dungeon.getLayout()
        playerDungeonPOS = app.playerCharacter.getDungeonPos()
        playerRoomPos = app.playerCharacter.getRoomPos()
        currentRoom = app.dungeon.getRoom(playerDungeonPOS[0], playerDungeonPOS[1]).getLayout()
        if event.key == 'm':
            app.map = not app.map
            
        elif event.key == 'Escape':
            app.gameState = 'pauseMenu'
            
        #movement
        if app.turn == 'player':
            if event.key == 'w':
                if app.playerCharacter.getRoomPos()[0] > 0:
                    if currentRoom[playerRoomPos[0]-1][playerRoomPos[1]] != 1:
                        app.playerCharacter.moveUpRoom()
                        app.playerMovesLeft -= 1
                else:
                    if grid[playerDungeonPOS[0]-1][playerDungeonPOS[1]] != 1:
                        app.playerCharacter.moveUpDungeon()
                        app.playerCharacter.setRoomPos(app.dungeon.getRoom(playerDungeonPOS[0]-1, playerDungeonPOS[1]).getSize()-1, playerRoomPos[1])
                pass
            
            elif event.key == 'a':
                if app.playerCharacter.getRoomPos()[1] > 0:
                    if currentRoom[playerRoomPos[0]][playerRoomPos[1]-1] != 1:
                        app.playerCharacter.moveLeftRoom()
                        app.playerMovesLeft -= 1
                else:
                    if grid[playerDungeonPOS[0]][playerDungeonPOS[1]-1] != 1:
                        app.playerCharacter.moveLeftDungeon()
                        app.playerCharacter.setRoomPos(playerRoomPos[0], app.dungeon.getRoom(playerDungeonPOS[0], playerDungeonPOS[1]-1).getSize()-1)
                pass
            
            elif event.key == 's':
                if app.playerCharacter.getRoomPos()[0] < app.dungeon.getRoom(playerDungeonPOS[0], playerDungeonPOS[1]).getSize()-1:
                    if currentRoom[playerRoomPos[0]+1][playerRoomPos[1]] != 1:
                        app.playerCharacter.moveDownRoom()
                        app.playerMovesLeft -= 1
                else:
                    if grid[playerDungeonPOS[0]+1][playerDungeonPOS[1]] != 1:
                        app.playerCharacter.moveDownDungeon()
                        app.playerCharacter.setRoomPos(0, playerRoomPos[1])
                pass
            
            elif event.key == 'd':
                if app.playerCharacter.getRoomPos()[1] < app.dungeon.getRoom(playerDungeonPOS[0], playerDungeonPOS[1]).getSize()-1:
                    if currentRoom[playerRoomPos[0]][playerRoomPos[1]+1] != 1:
                        app.playerCharacter.moveRightRoom()
                        app.playerMovesLeft -= 1
                else:
                    if grid[playerDungeonPOS[0]][playerDungeonPOS[1]+1] != 1:
                        app.playerCharacter.moveRightDungeon()
                        app.playerCharacter.setRoomPos(playerRoomPos[0], 0)
                pass
                
            #pickup/drop item using e
            elif event.key == 'q':
                if app.playerCharacter.currentWeapon != None:
                    if isinstance(currentRoom[playerRoomPos[0]][playerRoomPos[1]], Items):
                        if app.playerCharacter.weapons[app.playerCharacter.currentWeapon] == 0 and currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemType == 'Weapon':
                            weapons = app.playerCharacter.weapons
                            itemImage = currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage
                            itemImage = itemImage.resize(((app.sidebarActualWidth)//len(weapons)-20, (app.sidebarActualWidth)//len(weapons)-20), Image.Resampling.LANCZOS)
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage = itemImage
                            app.playerCharacter.pickupItem(currentRoom[playerRoomPos[0]][playerRoomPos[1]])
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]] = 0
                    else:
                        currentRoom[playerRoomPos[0]][playerRoomPos[1]] = app.playerCharacter.weapons[app.playerCharacter.currentWeapon]
                        app.playerCharacter.weapons[app.playerCharacter.currentWeapon] = 0
                        
                elif app.playerCharacter.currentArmor != None:
                    if isinstance(currentRoom[playerRoomPos[0]][playerRoomPos[1]], Items):
                        if app.playerCharacter.armor[app.playerCharacter.currentArmor] == 0 and currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemType == 'Armor':
                            armor = app.playerCharacter.armor
                            itemImage = currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage
                            itemImage = itemImage.resize(((app.sidebarActualWidth)//len(armor)-20, (app.sidebarActualWidth)//len(armor)-20), Image.Resampling.LANCZOS)
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage = itemImage
                            app.playerCharacter.pickupItem(currentRoom[playerRoomPos[0]][playerRoomPos[1]])
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]] = 0
                    else:
                        currentRoom[playerRoomPos[0]][playerRoomPos[1]] = app.playerCharacter.armor[app.playerCharacter.currentArmor]
                        app.playerCharacter.armor[app.playerCharacter.currentArmor] = 0
                        
                elif app.playerCharacter.currentItem != None:
                    if isinstance(currentRoom[playerRoomPos[0]][playerRoomPos[1]], Items):
                        if app.playerCharacter.miscItems[app.playerCharacter.currentItem] == 0 and currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemType == 'MiscItem':
                            miscItems = app.playerCharacter.miscItems
                            itemImage = currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage
                            itemImage = itemImage.resize(((app.sidebarActualWidth)//len(miscItems)-20, (app.sidebarActualWidth)//len(miscItems)-20), Image.Resampling.LANCZOS)
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]].itemImage = itemImage
                            app.playerCharacter.pickupItem(currentRoom[playerRoomPos[0]][playerRoomPos[1]])
                            currentRoom[playerRoomPos[0]][playerRoomPos[1]] = 0
                    else:
                        currentRoom[playerRoomPos[0]][playerRoomPos[1]] = app.playerCharacter.miscItems[app.playerCharacter.currentItem]
                        app.playerCharacter.miscItems[app.playerCharacter.currentItem] = 0
                        
            elif event.key == 'e':
                if app.playerCharacter.currentItem != None:
                    app.playerCharacter.useItem()
                
            
            #player turns
            if app.playerMovesLeft <= 0:
                app.turn = 'enemy'
                
            #update current room
            app.currentRoom = app.dungeon.getRoom(app.playerCharacter.getDungeonPos()[0],app.playerCharacter.getDungeonPos()[1])
            
        if app.playerCharacter.getDungeonPos() == app.endPointDungeon:
            if app.playerCharacter.getRoomPos() == app.dungeon.getRoom(app.endPointDungeon[0], app.endPointDungeon[1]).getEndPoint():
                app.gameState = 'win'    
    pass    

# def keyReleased(app, event): # use event.key
    # pass   

def mousePressed(app, event): # use event.x and event.y
    if app.gameState == 'start':
        (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
        if (row,col) in app.startGameButton:
            app.gameState = 'game'
        if (row,col) in app.characterSelectionButton:
            app.gameState = 'characterSelection'
            
    elif app.gameState == 'game':
        if event.x > app.gridWidth:
            (row,col) = getCell(event.x, event.y, app.sidebarActualWidth, app.sidebarActualWidth, len(app.playerCharacter.weapons)
                                , app.sidebarMinWidth, app.sidebarMinHeight+(app.gridWidth//app.dungeon.getSize()))
            if row == 0 and (col >= 0 and col < len(app.playerCharacter.weapons)):
                if app.playerCharacter.currentWeapon == col:
                    app.playerCharacter.currentWeapon = None
                else:
                    app.playerCharacter.currentWeapon = col
            if row == 1 and (col >= 0 and col < len(app.playerCharacter.armor)):
                if app.playerCharacter.currentArmor == col:
                    app.playerCharacter.currentArmor = None
                else:
                    app.playerCharacter.currentArmor = col
            if row == 2 and (col >= 0 and col < len(app.playerCharacter.miscItems)):
                if app.playerCharacter.currentItem == col:
                    app.playerCharacter.currentItem = None
                else:
                    app.playerCharacter.currentItem = col
        elif app.turn == 'player':
            if event.x <= app.gridWidth:
                (row,col) = getCell(event.x, event.y, app.gridWidth, app.gridHeight, app.currentRoom.getSize())
                if distance(row, col, app.playerCharacter.getRoomPos()[0], app.playerCharacter.getRoomPos()[1]) <= app.playerCharacter.movementSpeed:
                    if app.playerCharacter.currentWeapon != None:
                        if isinstance(app.currentRoom.getLayout()[row][col], Monster):
                            app.currentRoom.getLayout()[row][col].takeDamage(app.playerCharacter.dealDamage())
                            if app.currentRoom.getLayout()[row][col].getHealth() <= 0:
                                app.currentRoom.updateGrid(row, col, 0)
                            app.playerMovesLeft -= 1
        
    
    elif app.gameState == 'pauseMenu':
        (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
        if (row, col) in app.exitToStartButton:
            app.gameState = 'start'
        elif (row, col) in app.contineuGameButton:
            app.gameState = 'game'
        pass
    
    elif app.gameState == 'continueMenu':
        (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
        if (row, col) in app.exitToStartButton:
            app.gameState = 'start'
        elif (row, col) in app.contineuGameButton:
            app.gameState = 'game'
        pass
    
    elif app.gameState == 'deathScreen':
        (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
        if (row, col) in app.exitToStartButton:
            app.gameState = 'loadingScreen'
            appStarted(app, app.currentCharacter)
    
    elif app.gameState == 'characterSelection':
        characters = ['Default Character', 'Tony', 'Rinn', 'Drahkhan', 'Ruisheart']
        (row,col) = getCell(event.x, event.y, app.width, app.height, 10)
        if (row, col) in app.exitToStartButton:
            appStarted(app, app.currentCharacter)
        if app.charcterSelectionGrid[row][col] == 3:
            currentCharacterIndex = characters.index(app.currentCharacter)
            app.currentCharacter = characters[(currentCharacterIndex+1)%len(characters)]
        pass
    

# def mouseReleased(app, event): # use event.x and event.y
#     pass 

# def mouseMoved(app, event): # use event.x and event.y
#     pass    

# def mouseDragged(app, event): # use event.x and event.y
#     pass  


#######################################
###System Changes######################
#######################################
def updateRoomDimensions(app, room, width, height):
    for row in range(room.gridSize):
        for col in range(room.gridSize):
            if isinstance(room.grid[row][col],Monster):
                tempMonster = room.grid[row][col]
                spriteSheet = tempMonster.sprites
                tempMonster.sprites = updateSpriteDimensions(app, spriteSheet, app.gridWidth, app.gridHeight, room.gridSize) 
                # room.grid[row][col] = tempMonster
            elif isinstance(room.grid[row][col],Items):
                tempItem = room.grid[row][col]
                itemImage = resizeSprite(tempItem.itemImage, app.gridWidth//room.gridSize, app.gridHeight//room.gridSize)
                tempItem.itemImage = itemImage
    pass

def doAnimations(app):
    app.playerCharacter.animateSprite()
    app.currentRoom.animateRoom()

def timerFired(app): # respond to timer events
    if app.gameState == 'game':
        if app.playerCharacter.getHealth() <= 0:
            app.gameState = 'deathScreen'
            
        #handle animations and other time stuff
        app.animationTimer += app.framerate
        if app.animationTimer >= 100:
            app.animationTimer = 0
            doAnimations(app)
            # monster turns
            if app.turn == 'enemy':
                app.currentRoom.tick(app.playerCharacter)
                app.turn = 'player'

    if app.gameState == 'win':
        continueGame(app)
        app.gameState = 'continueMenu'
        pass
    pass           

def sizeChanged(app): # respond to window size changes
    initDimensions(app)
    initStartMenu(app)
    doAnimations(app)
    app.playerCharacter.updateSprite(updateSpriteDimensions(app, app.playerCharacter.getSprites()
                                                            , app.gridWidth, app.gridHeight, app.dungeon.getSize()))
    #update weapon dimensions
    updateItemDimensions(app, app.playerCharacter, app.sidebarActualWidth, app.sidebarActualWidth, len(app.playerCharacter.weapons))
    updateRoomDimensions(app, app.currentRoom, app.gridWidth, app.gridHeight)

    pass  

            
runApp(width = 1200, height = 800, title = '15-112: Fail Early and Often')
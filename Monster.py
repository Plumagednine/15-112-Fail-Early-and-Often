from cmu_112_graphics import *
from helpers import *
# It's a class that represents a monster in the game.
# """
# It takes a dictionary of monster attributes and assigns them to the monster object

# :param monsterDict: A dictionary containing all the information about the monster
# """
class Monster:
    def __init__(self, monsterDict):
        self.sprites = monsterDict.get("spriteSheet")
        self.roomRow = monsterDict.get("roomRow")
        self.roomCol = monsterDict.get("roomColumn")
        self.totalHP = monsterDict.get("hitPoints")
        self.currentHP = monsterDict.get("hitPoints")
        self.strengthModifier = (monsterDict.get("strength")-10)//2
        self.movementSpeed = monsterDict.get("movementSpeed")//10
        self.spriteCounter = monsterDict.get("spriteCounter")
        self.monsterName = monsterDict.get("monsterName")
        self.step = 0
        self.tickCounter = 0
    
    
#######################################
###Graphics Functions##################
#######################################

    def drawMonster(self, app, canvas, roomSize):
        (x, y) = self.getRoomPos()
        (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, roomSize)
        cellWidth = app.gridWidth // roomSize
        cellHeight = app.gridHeight // roomSize
        healthBarMultiplier = self.currentHP/self.totalHP
        canvas.create_rectangle(x0,y0,x1,y0+cellHeight//10, fill='#f71735')
        canvas.create_rectangle(x0,y0,x0+(cellWidth*healthBarMultiplier),y0+cellHeight//10, fill='#44af69')
        canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, image=ImageTk.PhotoImage(self.getImage()))
        pass
    
    def animateSprite(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
        pass
    
    def updateSprite(self, spriteSheet):
        self.sprites = spriteSheet
        pass
    
    def getSprites(self):
        return self.sprites
    
    def getImage(self):
        return self.sprites[self.spriteCounter]
    
      
###############################################
###Room Movement and Location Functions########
###############################################
    
    def getRoomPos(self):
        return (self.roomRow, self.roomCol)
    
    def setRoomPos(self, row, col):
        self.roomRow = row
        self.roomCol = col
        pass
    
    def moveUpRoom(self):
        self.roomRow -= 1
        pass
    
    def moveDownRoom(self):
        self.roomRow += 1
        pass
    
    def moveLeftRoom(self):
        self.roomCol -= 1
        pass
        
    def moveRightRoom(self):
        self.roomCol += 1
        pass

#######################################
###Health and Damage Functions#########
#######################################

    def getHealth(self):
        return self.currentHP
    
    def takeDamage(self, damage):
        if self.currentHP - damage <= 0:
            self.currentHP = 0
        else:
            self.currentHP -= damage
        pass
    
    def dealDamage(self):
        return self.strengthModifier + random.randint(1, 3)
    
#######################################
###Tick Functions######################
#######################################

    def tick(self, player, roomLayout):
        path = None
        offset = 2
        playerPos = player.getRoomPos()
        if lineOfSight(self.getRoomPos(), playerPos, roomLayout):
            path = aStar(self.getRoomPos(), playerPos, roomLayout)
            self.tickCounter += 1
        
        if distance(self.getRoomPos()[0],self.getRoomPos()[1], playerPos[0], playerPos[1]) <= self.movementSpeed and self.tickCounter == 1:
            player.takeDamage(self.dealDamage())
            self.step = 0
            self.tickCounter = 0
            
        if path and self.tickCounter == 1:
            if self.step >= len(path):
                self.step = 0
            move = path[self.step]
            self.setRoomPos(move[0], move[1])
            self.step += 1
            self.tickCounter = 0
            
        return self.getRoomPos()
            
        
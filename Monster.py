from cmu_112_graphics import *
from helpers import *

class Monster:
    def __init__(self, monsterDict):
        self.sprites = monsterDict.get("spriteSheet")
        self.roomRow = monsterDict.get("roomRow")
        self.roomCol = monsterDict.get("roomColumn")
        self.totalHP = monsterDict.get("hitPoints")
        self.currentHP = monsterDict.get("hitPoints")
        self.strengthModifier = (monsterDict.get("strength")-10)//2
        self.movementSpeed = monsterDict.get("movementSpeed")
        self.spriteCounter = monsterDict.get("spriteCounter")
        self.monsterName = monsterDict.get("monsterName")
    
    
#######################################
###Graphics Functions##################
#######################################

    def drawMonster(self, app, canvas, roomSize):
        (x, y) = self.getRoomPos()
        (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, roomSize)
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
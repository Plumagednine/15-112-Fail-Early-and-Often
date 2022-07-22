from cmu_112_graphics import *
from helpers import *
from Items import *

class Player:
    def __init__(self, playerDict):
        self.sprites = playerDict.get("spriteSheet")
        self.spriteCounter = 0
        self.row = playerDict.get("row")
        self.col = playerDict.get("column")
        self.totalHP = playerDict.get("hitPoints")
        self.currentHP = playerDict.get("hitPoints")
        self.strength = playerDict.get("strength")
        self.dexterity = playerDict.get("dexterity")
        self.constitution = playerDict.get("constitution")
        self.movementSpeed = playerDict.get("movementSpeed")
        self.weapons = [0]*5
        for i in range(len(playerDict.get("weapons"))):
            self.weapons[i] = playerDict.get("weapons")[i]
        self.currentWeapon = 0
        self.armor = [0]*5
        for i in range(len(playerDict.get("armor"))):
            self.armor[i] = playerDict.get("armor")[i]
        self.miscItems = [0]*5
        for i in range(len(playerDict.get("miscItems"))):
            self.miscItems[i] = playerDict.get("miscItems")[i]
        self.currentItem = 0
        print(self.weapons, self.armor, self.miscItems)
        pass
    
#######################################
###Graphics Functions##################
#######################################

    def drawPlayer(self, app, canvas):
        (x, y) = self.getPos()
        (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
        canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, image=ImageTk.PhotoImage(self.getImage()))
        pass
    
    def animateSprite(self, app):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
        pass
    
    def updateSprite(self, spriteSheet):
        self.sprites = spriteSheet
        pass
    
    def getSprites(self):
        return self.sprites
    
    def getImage(self):
        return self.sprites[self.spriteCounter]
    
#######################################
###Movement and Location Functions#####
#######################################
    
    def getPos(self):
        return (self.row, self.col)
    
    def setPos(self, row, col):
        self.row = row
        self.col = col
        pass
    
    def moveUp(self):
        self.row -= 1
        pass
    
    def moveDown(self):
        self.row += 1
        pass
    
    def moveLeft(self):
        self.col -= 1
        pass
        
    def moveRight(self):
        self.col += 1
        pass

#######################################
###Health and Damage Functions#########
#######################################

    def getHealth(self):
        return self.currentHP
    
    def getHealthMultiplyer(self):
        return self.currentHP/self.totalHP
    
    def takeDamage(self, damage):
        if self.currentHP - damage <= 0:
            self.currentHP = 0
        else:
            self.currentHP -= damage
        pass
            
    def heal(self, heal):
        if self.currentHP + heal >= self.totalHP:
            self.currentHP = self.totalHP
        else:
            self.currentHP += heal
        pass
    
    def dealDamage(self):
        return self.strength

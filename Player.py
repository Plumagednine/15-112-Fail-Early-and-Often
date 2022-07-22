from cmu_112_graphics import *
from helpers import *

class Player:
    def __init__(self, row = 0, col = 0, spriteSheet = '', spriteCounter = 0, hitPoints = 100
                 , strength = 10, dexterity = 10, constitution = 10
                 , movementSpeed = 30):
        self.sprites = spriteSheet
        self.spriteCounter = spriteCounter
        self.row = row
        self.col = col
        self.totalHP = hitPoints
        self.currentHP = hitPoints
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.movementSpeed = movementSpeed
        self.inventory = []
        pass
    
    def drawPlayer(self, app, canvas):
        (x, y) = self.getPos()
        (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
        canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, image=ImageTk.PhotoImage(self.getImage()))
        pass
    
    def animateSprite(self, app):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
        pass
    
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
    
    def updateSprite(self, spriteSheet):
        self.sprites = spriteSheet
        pass
    
    def getSprites(self):
        return self.sprites
    
    def getImage(self):
        return self.sprites[self.spriteCounter]
    
    def getHealth(self):
        return self.currentHP
    
    def getHealthMultiplyer(self):
        return self.currentHP/self.totalHP
    
    def takeDamage(self, damage):
        if self.currentHP - damage <= 0:
            self.currentHP = 0
        else:
            self.currentHP -= damage

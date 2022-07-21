from cmu_112_graphics import *


class Player:
    def __init__(self, row = 0, col = 0, token = '', hitPoints = 100
                 , strength = 10, dexterity = 10, constitution = 10
                 , movementSpeed = 30):
        self.sprite = token
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
    
    def updateSprite(self, token):
        self.sprite = token
        pass
    
    def getImage(self):
        return self.sprite
    
    def getHealth(self):
        return self.currentHP
    
    def getHealthMultiplyer(self):
        return self.currentHP/self.totalHP
    
    def takeDamage(self, damage):
        if self.currentHP - damage <= 0:
            self.currentHP = 0
        else:
            self.currentHP -= damage

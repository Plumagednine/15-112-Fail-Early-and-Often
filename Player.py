from cmu_112_graphics import *


class Player:
    def __init__(app, row = 0, col = 0, token = '', hitPoints = 100
                 , strength = 10, dexterity = 10, constitution = 10
                 , movementSpeed = 30):
        app.sprite = token
        app.row = row
        app.col = col
        app.totalHP = hitPoints
        app.currentHP = hitPoints
        app.strength = strength
        app.dexterity = dexterity
        app.constitution = constitution
        app.movementSpeed = movementSpeed
        app.inventory = []
        
        pass
    
    def getPos(app):
        return (app.row, app.col)
    
    def setPos(app, row, col):
        app.row = row
        app.col = col
        pass
    
    def moveUp(app):
        app.row -= 1
        pass
    
    def moveDown(app):
        app.row += 1
        pass
    
    def moveLeft(app):
        app.col -= 1
        pass
        
    def moveRight(app):
        app.col += 1
        pass
    
    def updateSprite(app, token):
        app.sprite = token
        pass
    
    def getImage(app):
        return app.sprite
    
    def getHealth(app):
        return app.currentHP
    
    def getHealthMultiplyer(app):
        return app.currentHP/app.totalHP
    
    def takeDamage(app, damage):
        if app.currentHP - damage <= 0:
            app.currentHP = 0
        else:
            app.currentHP -= damage

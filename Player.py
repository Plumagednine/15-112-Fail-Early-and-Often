from cmu_112_graphics import *


class Player:
    def __init__(app, row = 0, col = 0, token = ''):
        app.sprite = token
        app.row = row
        app.col = col
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

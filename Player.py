from cmu_112_graphics import *


class Player:
    #######################################
    ###Helper Functions####################
    #######################################

    def almostEqual(self, d1, d2, epsilon=10**-7): #helper-fn
        # note: use math.isclose() outside 15-112 with Python version 3.5 or later
        return (abs(d2 - d1) < epsilon)

    def roundHalfUp(self, d): #helper-fn
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def create_elipse(self, canvas, cx, cy, radius, **options):
        canvas.create_oval(cx - radius
                        , cy - radius
                        , cx + radius
                        , cy + radius
                        , **options)

    def getCell(self, x, y, width, height, gridSize):
        cellWidth = width // gridSize
        cellHeight = height // gridSize
        row =  y//cellHeight
        col = x//cellWidth
        return (row, col)

    def getCellBounds(self, row, col, width, height, gridSize):
        cellWidth = width // gridSize
        cellHeight = height // gridSize
        x0 = col * cellWidth
        y0 = row * cellHeight
        x1 = (col+1) * cellWidth
        y1 = (row+1) * cellHeight
        return (x0, y0, x1, y1)
    
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
    
    #######################################
    ###Initalizer Function#################
    #######################################
    def drawPlayer(self, app, canvas):
        (x, y) = self.getPos()
        (x0, y0, x1, y1) = self.getCellBounds(x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
        canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, pilImage = self.getImage())
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

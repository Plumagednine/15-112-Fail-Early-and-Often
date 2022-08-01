from cmu_112_graphics import *
from helpers import *
from Items import *

class Player:
    def __init__(self, playerDict, allItemsDictionary):
        self.sprites = playerDict.get("spriteSheet")
        self.dungeonRow = playerDict.get("dungeonRow")
        self.dungeonCol = playerDict.get("dungeonColumn")
        self.roomRow = playerDict.get("roomRow")
        self.roomCol = playerDict.get("roomColumn")
        self.totalHP = playerDict.get("hitPoints")
        self.currentHP = playerDict.get("hitPoints")
        self.strengthModifier = (playerDict.get("strength")-10)//2
        self.dexterityModifier = (playerDict.get("dexterity")-10)//2
        self.constitutionModifier = (playerDict.get("constitution")-10)//2
        self.movementSpeed = playerDict.get("movementSpeed")//10
        self.spriteCounter = playerDict.get("spriteCounter")
        self.allItems = allItemsDictionary
        #######################################
        ###Weapon Inventory####################
        #######################################
        self.weapons = [0]*5
        for i in range(len(playerDict.get("weapons"))):
            self.weapons[i] = self.allItems.get(playerDict.get("weapons")[i])
        self.currentWeapon = 0
        #######################################
        ###Armor Inventory#####################
        #######################################
        self.armor = [0]*5
        for i in range(len(playerDict.get("armor"))):
            self.armor[i] = self.allItems.get(playerDict.get("armor")[i])
        self.currentArmor = None
        #######################################
        ###Miscellaneous Items Inventory#######
        #######################################
        self.miscItems = [0]*5
        for i in range(len(playerDict.get("miscItems"))):
            self.miscItems[i] = self.allItems.get(playerDict.get("miscItems")[i])
        self.currentItem = None
        pass
    
#######################################
###Graphics Functions##################
#######################################

    def drawPlayer(self, app, canvas, mapShowing):
        if mapShowing:
            (x, y) = self.getDungeonPos()
            (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
            canvas.create_image(x0 + (x1-x0)//2, y0 + (y1-y0)//2, image=ImageTk.PhotoImage(self.getImage()))
        else:
            (x, y) = self.getRoomPos()
            (x0, y0, x1, y1) = getCellBounds(x, y, app.gridWidth, app.gridHeight, app.dungeon.getSize())
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
###Dungeon Movement and Location Functions#####
###############################################
    
    def getDungeonPos(self):
        return (self.dungeonRow, self.dungeonCol)
    
    def setDungeonPos(self, row, col):
        self.dungeonRow = row
        self.dungeonCol = col
        pass
    
    def moveUpDungeon(self):
        self.dungeonRow -= 1
        pass
    
    def moveDownDungeon(self):
        self.dungeonRow += 1
        pass
    
    def moveLeftDungeon(self):
        self.dungeonCol -= 1
        pass
        
    def moveRightDungeon(self):
        self.dungeonCol += 1
        pass
    
      
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
###Item Functions######################
#######################################
    def pickupItem(self, item):
        if item.getItemType() == 'Weapon':
            self.weapons[self.currentWeapon] = item
        elif item.getItemType() == 'Armor':
            self.armor[self.currentArmor] = item
        elif item.getItemType() == 'MiscItem':
            self.miscItems[self.currentItem] = item
    
    def dropItem(self):
        return (self.weapons[self.currentWeapon], self.armor[self.currentArmor], self.miscItems[self.currentItem])
        

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
    
    def useItem(self):
        useageInfo = self.miscItems[self.currentItem].useItem()
        if useageInfo[0] == 'Health':
            self.heal(useageInfo[1])
        self.miscItems[self.currentItem] = 0
    
    def dealDamage(self):
        if self.weapons[self.currentWeapon].itemModifier == 'Dexterity':
            return self.dexterityModifier + random.randint(1,self.weapons[self.currentWeapon].itemModifierValue)
        elif self.weapons[self.currentWeapon].itemModifier == 'Strength':
            return self.strengthModifier + random.randint(1,self.weapons[self.currentWeapon].itemModifierValue)
      

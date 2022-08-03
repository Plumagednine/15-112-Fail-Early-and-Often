from cmu_112_graphics import *
from helpers import *

# It's a class that creates an item object that can be used in the game.
# """
# It takes a dictionary and assigns the values to the variables.

# :param itemDict: A dictionary containing all the information about the item
# """
class Items:
    def __init__(self, itemDict):
        self.itemName = itemDict.get('itemName')
        self.itemType = itemDict.get('itemType')
        self.maxStackSize = itemDict.get('maxStackSize')
        self.itemModifier = itemDict.get('itemModifier')
        self.itemModifierValue = itemDict.get('itemModifierValue')
        self.itemImage = itemDict.get('itemImagePath')
        self.item = itemDict
        pass

    def getItem(self):
        return self.item
        pass
    
    def getItemImage(self):
        return self.itemImage

    def setItemImage(self, image):
        self.itemImage = image
    
    def getItemType(self):
        return self.itemType

    def useItem(self):
        return self.itemModifier, self.itemModifierValue
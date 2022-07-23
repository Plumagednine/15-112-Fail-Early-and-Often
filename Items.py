from cmu_112_graphics import *
from helpers import *


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

import imp
from cmu_112_graphics import *
from helpers import *


class Items:
    def __init__(self, itemName, itemType, itemDescription, maxStackSize, itemModifier, itemModifierValue, itemImage):
        self.itemName = itemName
        self.itemType = itemType
        self.itemDescription = itemDescription
        self.maxStackSize = maxStackSize
        self.itemModifier = itemModifier
        self.itemModifierValue = itemModifierValue
        self.item = {
            "itemName": self.itemName,
            "itemImage": self.itemImage,
            "itemType": self.itemType,
            "itemDescription": self.itemDescription,
            "maxStackSize": self.maxStackSize,
            "itemModifier": self.itemModifier,
            "itemModifierValue": self.itemModifierValue   
        }
        pass

    def getItem(self):
        return self.item
        pass
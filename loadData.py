from cmu_112_graphics import *
from helpers import *
from Items import *
from Player import *


def loadItems():
    items = loadJSON('gameData\items.JSON')
    allItemsDictionary = {}
    for item in items:
        itemDict = item
        allItemsDictionary[itemDict.get('itemName')] = Items(itemDict)
    return allItemsDictionary

def loadPlayerCharacters(allItemsDictionary):
    characters = loadJSON('gameData\characters.JSON')
    allCharactersDictionary = {}
    for character in characters:
        characterDict = character
        allCharactersDictionary[characterDict.get('characterName')] = Player(characterDict, allItemsDictionary)
    return allCharactersDictionary
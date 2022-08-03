from cmu_112_graphics import *
from helpers import *
from Items import *
from Player import *
from Monster import *
from Room import *

# """
# It takes a JSON file, converts it to a dictionary, and then creates an object for each item in the
# dictionary
# :return: A dictionary of all the things in the game.
# """
def loadItems():
    items = loadJSON('gameData/items.JSON')
    allItemsDictionary = {}
    for item in items:
        itemDict = item
        allItemsDictionary[itemDict.get('itemName')] = Items(itemDict)
    return allItemsDictionary

def loadPlayerCharacters(allItemsDictionary):
    characters = loadJSON('gameData/characters.JSON')
    allCharactersDictionary = {}
    for character in characters:
        characterDict = character
        allCharactersDictionary[characterDict.get('characterName')] = Player(characterDict, allItemsDictionary)
    return allCharactersDictionary

def loadMonsters():
    monsters = loadJSON('gameData/monsters.JSON')
    allMonstersDictionary = {}
    for monster in monsters:
        monsterDict = monster
        allMonstersDictionary[monsterDict.get('monsterName')] = Monster(monsterDict)
    return allMonstersDictionary

def loadRooms(app, allMonstersDictionary, allItemsDictionary):
    rooms = loadJSON('gameData/rooms.JSON')
    allRoomsDictionary = {}
    for room in rooms:
        roomDict = room
        allRoomsDictionary[roomDict.get('roomId')] = Room(app, roomDict, allMonstersDictionary, allItemsDictionary)
    return allRoomsDictionary
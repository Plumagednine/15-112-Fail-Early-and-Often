from cmu_112_graphics import *
from helpers import *
from Items import *
from Player import *
from Monster import *
from Room import *

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

def loadRooms():
    rooms = loadJSON('gameData/rooms.JSON')
    allRoomsDictionary = {}
    for room in rooms:
        roomDict = room
        allRoomsDictionary[roomDict.get('roomId')] = Room(roomDict)
    return allRoomsDictionary
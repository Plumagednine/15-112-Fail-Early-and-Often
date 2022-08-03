import json
import os
from random import randint
from helpers import *

allItemImagePaths = []
newItemsDictionary = []
weaponModifiers = ["Strength", "Dexterity"]
basePath = "textures/armor/Gloves"
for path in os.scandir(basePath):
    if path.is_file():
        allItemImagePaths.append(basePath+path.name)
        newItemsDictionary.append(
            {'itemName': path.name.split(".")[0], 
            'itemType': 'Armor', 
            'maxStackSize': 1, 
            'itemModifier': 'Constitution', 
            'itemModifierValue': random.randint(1,10), 
            'itemImagePath': basePath+"/"+path.name}
        )
print2dList(newItemsDictionary)
# Serializing json
json_object = json.dumps(newItemsDictionary, indent=4)
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

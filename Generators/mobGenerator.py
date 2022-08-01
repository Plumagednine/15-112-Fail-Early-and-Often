from ast import Import
import json
import os
import random
import os
import os
from PIL import Image

def print2dList(list):
    for row in list:
        print(row)

allMobImagePaths = []
newItemsDictionary = []
weaponModifiers = ["Strength", "Dexterity"]
basePath = "monsterSprites/"
for path in os.scandir(basePath):
    if path.is_file():
        allMobImagePaths.append(basePath+path.name)
        newItemsDictionary.append({
        "monsterName": path.name.split(".")[0],
        "roomRow": 1,
        "roomColumn": 1,
        "spriteSheet": basePath+"/"+path.name,
        "spriteCounter": 0,
        "hitPoints": random.randint(1,20),
        "strength": random.randint(10,16)
        })
print2dList(newItemsDictionary)
# Serializing json
json_object = json.dumps(newItemsDictionary, indent=4)
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

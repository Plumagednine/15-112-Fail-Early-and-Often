from cmu_112_graphics import *
from helpers import *
from Player import *

class Monster(Player):
    def __init__(self, playerDict, allItemsDictionary):
        super().__init__(playerDict, allItemsDictionary)
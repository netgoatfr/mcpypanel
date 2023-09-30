import uuid
import nbtlib
import time
import os
class Player:
    def __init__(self,path,uuid):
        self.path = path+"/playerdata"+str(uuid)
        self.nbt = nbtlib.load(self.path+"/level.data")

class World:
    def __init__(self,dir,world_name):
        self.path = dir+"/"+world_name
        self.nbt = nbtlib.load(self.path+"/level.dat")
        self.players = {}
    def _refresh(self):
        for u in os.listdir(self.path+"/playerdata"):
            u = uuid.UUID(u)
            self.players[u] = Player(path,u)
            
import uuid
import nbtlib

class WorldNbt:
    def __init__(self,dir,name="level.nbt"):
        self.path = path+"/"+name
        self.file = nbtlib.load(self.path))
    def __getattr__(self,attr):
        return self.file[attr]
    def __setattr__(self,attr,data):
        self.file[attr]=data
        self.file.save()
    def __delattr__(self,attr):
        raise NotImplementedError
class World:
    def __init__(self,dir,world_name):
        self.path = dir+"/"+world_name
        self.nbt = WorldNbt(self.path)

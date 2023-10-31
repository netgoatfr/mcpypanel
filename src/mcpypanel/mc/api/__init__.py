import uuid
import nbtlib
import time
import os
import mcrcon

class PlayerNbt:
    def __init__(self,path,id,world):
        self.path = path+"playerdata/"+str(id)+".dat"
        self.nbt = nbtlib.load(self.path)
        self.uuid = id
        self.world = world
        self.rcon = self.world.server.rcon
        self.playername = self.nbt["bukkit"]["lastKnownName"]
    def _refresh(self):
        self.nbt = nbtlib.load(self.path)
    @property
    def pos(self):
        self._refresh()
        return (float(self.nbt["Pos"][0]),float(self.nbt["Pos"][1]),float(self.nbt["Pos"][2]))
    def set_pos(self,*,x,y,z):
        try:
            with self.rcon:
                rcon.command("tp "+self.playername+str(x)+" "+str(y)+" "+str(z))
                return True
        except:
            return False
        
class World:
    def __init__(self,dir,world_name,server):
        self.name = world_name
        self.path = os.path.join(dir,world_name)
        self.server = server
        self.nbt = nbtlib.load(self.path+"/level.dat")
        self.players = []
        self._check_players()
        
    def _refresh(self):
        self.nbt = nbtlib.load(self.path+"level.dat")
    def _refresh_all_players(self):
        """
        Can be laggy, depend of the number of player
        """
        self._check_players()
        for player in self.players:
            player._refresh()
    def _get_player(self,uuid_or_playername):
        for player in self.players:
            if player.uuid == uuid_or_playername or player.playername == uuid_or_playername:
                return player
    def _check_players(self):
        for i in os.listdir(self.path+"playerdata"):
            p,e = os.path.splitext(i)
            if e == ".dat":
                if p not in self.players:
                    try:
                        u = uuid.UUID(p)
                    except:
                        continue
                    p = Player(self.path,u,self)
                    self.players[p.playername] = p


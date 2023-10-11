import uuid
import nbtlib
import time
import os

class Player:
    def __init__(self,path,d):
        self.path = path+"playerdata/"+str(d)+".dat"
        self.nbt = nbtlib.load(self.path)
        self.uuid = d
        self.playername = self.nbt["bukkit"]["lastKnownName"]
    def _refresh(self):
        self.nbt = nbtlib.load(self.path)
    @property
    def pos(self):
        return (float(self.nbt["Pos"][0]),float(self.nbt["Pos"][1]),float(self.nbt["Pos"][2]))
    @pos.setter
    def pos(self,*,x=None,y=None,z=None):
        final_pos = (x if x is not None else self.nbt["Pos"][0],y if y is not None else self.nbt["Pos"][1],z if z is not None else self.nbt["Pos"][2])
        self.nbt["Pos"] = final_pos
        self.nbt.save()
        
class World:
    def __init__(self,dir,world_name):
        self.path = dir+"/"+world_name+"/"
        self.nbt = nbtlib.load(self.path+"level.dat")
        self.players = []
        self._check_players()
        
    def _refresh(self):
        self.nbt = nbtlib.load(self.path+"level.dat")
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
                    u = uuid.UUID(p)
                    self.players.append(Player(self.path,u))
        
        
        
        
class Server:
    def __init__(self,parent,path,servername,jar_name="server"):
        self.parent = parent
        self.path = path
        self.jar_path = self.path+"/"+jar_name+".jar"
        if not os.path.exists(self.jar_path):
            self.log.fatal("Jar file not found.")
            self._found = False
            return
        self._ever_started = os.path.exists(self.path+"/"+"server.properties")
        if self.self._ever_started:
            self.world = World(self.path,"world")
        self._found = True
        self.running = True
    def start(self):
        if self.parent.tmux_serv.has_session("server."+self.servername):
            self.log.info("Server is already running!")
            return
        self.session = self.parent.tmux_serv.new_session("server."+self.servername)
        self.session.cmd("java -jar "+self.parent.config["per-server-java-args"] or ""+" "+self.jar_path)
        
        
            
        
        
        
        
        
        
        
def get_time(func,*args,**kwargs):
    t1=time.time()
    func(*args,**kwargs)
    return(time.time()-t1)
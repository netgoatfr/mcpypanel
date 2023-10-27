import uuid
import nbtlib
import time
import os
import mcrcon

class Player:
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
        with self.rcon:
            rcon.command("tp "+self.playername+str(x)+" "+str(y)+" "+str(z))
        
class World:
    def __init__(self,dir,world_name,server):
        self.path = dir+"/"+world_name+"/"
        self.server = server
        self.nbt = nbtlib.load(self.path+"level.dat")
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
        self.rcon = mcrcon.MCRcon(self.parent.config["servers"][servername]["ip"],self.parent.config["servers"][servername]["rcon_port"],self.parent.config["servers"][servername]["rcon-password"])
        if self.self._ever_started:
            self.world = World(self.path,"world",self)
        self._found = True
        self.running = True
    def start(self):
        if self.parent.tmux_serv.has_session("server."+self.servername):
            self.log.error("Server is already running!")
            return
        self.session = self.parent.tmux_serv.new_session("server."+self.servername)
        self.session.cmd("java -jar "+self.parent.config["per-server-java-args"] or ""+" "+self.jar_path)
    def stop(self):
        if not self.parent.tmux_serv.has_session("server."+self.servername):
            self.log.eror("Server is not running!")
            return
        with self.rcon:
            if self.parent.config["servers"]["warn-before-stop"]:
                self.command("") # TO-Do
                sleep(5)
            self.command("stop")
    def command(self,cmd):
        if not self.parent.tmux_serv.has_session("server."+self.servername):
            self.log.eror("Server is not running!")
            return 
        return self.rcon.command(cmd)      
            
        
        
        
class Proxy:
    def __init__(self,*a):pass
        
        
        
def get_time(func,*args,**kwargs):
    t1=time.time()
    func(*args,**kwargs)
    return(time.time()-t1)

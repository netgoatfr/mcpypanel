import uuid
import nbtlib
import time
import os
import mcrcon
from .mojang import MojangApi
from .api import *

class PlayerCache:
    def __init__(self,server,datas):
        self.api = MojangApi()
        self.id = datas["id"]
        self.ip = datas["ip"]
        self.port = datas["port"]
        self.spawn_world = datas["spawn_world"]
        self.spawn_x = datas["spawn_x"]
        self.spawn_y = datas["spawn_y"]
        self.spawn_z = datas["spawn_z"]
        self.name = datas["player"]
        self.server = server
        self.cache_db = self.server.parent.storify.getDB("player_cache")

        try:
            self.profile = self.api.get_profile_from_id(self.id)
        except TypeError:
            self.profile = None
            self.cracked_account = True
        else:
            self.cracked_account = False
        self.nbt = PlayerNbt(server.path,self.id,self.server._get_world(self.spawn_world))
        self.cache_db[self.id] = dict(name=self.name,cracked=self.cracked_account,**datas)


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
            self._get_worlds()
        self._found = True
        self.running = True
        self.players = []

        @self.parent.events.on("server."+servername+".logwatch.user_logged")
        def on_user_logged(datas):
            self.players.append(PlayerCache(self,datas))
            
    def _get_worlds(self):
        self.worlds = []
        for folder in os.listdir(self.path):
            if "level.dat" in os.listdir(os.path.join(self.path,folder)):
                self.worlds.append(World(self.path,folder,self))
    def _get_world(self,name):
        for w in self.worlds:
            if w.name == name:
                return w
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

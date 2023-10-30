import uuid
import nbtlib
import time
import os
import mcrcon

class PlayerCache:
    def __init__(self,)

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

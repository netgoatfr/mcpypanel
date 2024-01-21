import os
import subprocess
import __init__

class ProcessError(Exception):pass

class ProcessAlreadyRunning(ProcessError):pass
class ProcessNotRunning(ProcessError):pass
class ProcessDosentExists(ProcessError):pass


class Process:
    def __init__(self,parent,name,cmd,deamon=False):
        self.cmd = cmd
        self.deamon = deamon
        self.pid = None
        self.parent:__init__.Panel = parent
    def start(self):
        if self.running:
            raise ProcessAlreadyRunning("This process is already running.")
        
        inp = self._make_pipe(self.name+"-input")
        out = self._make_pipe(self.name+"-output")
        
        if self.deamon:
            os.system(f'nohup "{self.cmd}" &>{out} &')
        elif:
            os.system(f'{self.cmd} &>{out} &')
        self.pid = int(os.popen)
        
        
    def _make_pipe(self,name):
        if not os.path.exists(os.join(self.parent._BASE_DIR,"pipes")):
            os.mkdir(os.join(self.parent._BASE_DIR,"pipes"))
        os.system("mkfifo "+os.join(self.parent._BASE_DIR,"pipes",name+".pipe"))
        return os.join(self.parent._BASE_DIR,"pipes",name+".pipe")
    def _del_pipe(self,name):
        if not os.path.exists(os.join(self.parent._BASE_DIR,"pipes")):
            os.mkdir(os.join(self.parent._BASE_DIR,"pipes"))
        os.remove(os.join(self.parent._BASE_DIR,"pipes",name+".pipe"))
        
        
    def stop(self):
        if not self.running:
            ProcessNotRunning("This process is not running.")
    
    @property
    def _dir(self):
        if self.pid is not None:
            return os.join("/proc",self.pid)
    
    @property
    def running(self):
        if self.pid is not None:
            if os.path.exists(self._dir):
                return True
        return False
    
    @property
    def cwd(self):
        if self.pid is not None:
            return os.readlink(os.join(self._dir,"cwd"))
        
        
    @staticmethod
    def _get_from_pid(pid):
        # Experimental
        path = os.join("/proc",pid)
        if not os.path.exists(path):
            raise ProcessDosentExists
        p = Process("")
        p.pid = pid

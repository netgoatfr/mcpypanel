"""

    __init__.py file

    Load all core modules

"""

from .logger import Logger
from .config import ConfFile
from .wizard import Wizard
from .events import Events
from .console import Console
from .dashboard import Dashboard
from .minecraft.proxy import *
from .minecraft.server import *
from .__version__ import *
import libtmux
import sys
import os

class Panel:
    def __init__(self,args):

        ### Useful variables

        self.log = Logger("Panel")
        self._BASE_DIR = os.path.split(args[0])[0]
        self._DIR = self._BASE_DIR + "mcpypanel_data"
        self._args = args

        self._first_time = False
        self.debug = False
        self._abort_startup = False
        self._return_code = 0
        
        self.banner = BANNER
        self._banner_size = _BANNER_SIZE()
        #################################################################################################

        ### SETUP

        if not os.path.exists(self._DIR) or not os.path.isdir(self._DIR) or not os.listdir(self._DIR):
            self._first_time = True
        else:
            self.config = ConfFile(self)
            if self._abort_startup:
                self._return_code = 1
                return
            self.debug = self.config["debug"]
            self.logger.colored_output = self.config["colored_output"]
            if self.config["reset_panel"]:self._first_time = True
        if self._first_time:
            Wizard(self).run()

        ################################################################################################

        self.events = Events()

        self.dashboard = None
        self.remote_controle = None
        
        self.tmux_serv = libtmux.Server("mcpypanel",color=True)
        
        self.run()

    def run(self):
        ###########################################
        print("#"*self._banner_size[0])
        print(self._banner)
        print("#"*self._banner_size[0])
        ###########################################
        
        
        self.log.info("Welcome to McPyPanel! Starting...")
        
        if self.config["dashbord"]["autorun"]:
            self.log.info("Auto-starting the web-based dashboard... (you can disable it the config)")
            self.dashboard = Dashboard(self)
        if self.config["remotecontrol"]["autorun"]:
            self.log.info("Auto-starting the remote control... (you can disable it the config)")
            self.remote_control = RemoteControl(self)

        if self.config["minecraft"]["with_proxy"]:
            self._with_proxy = True
            self.proxy = Proxy(self)
            if not self._proxy._found:
                self.log.fatal("Proxy not found. Aborting startup.")
                self._return_code = 1
                return
            self.log.info("The proxy and all the servers are loaded!")
        else:
            self._with_proxy = False
            self.server = Server(self,"./")
            if not self._server._found:
                self.log.fatal("Server not found. Aborting startup.")
                self._return_code = 1
                return
            self.log.info("Server Loaded")

        if self._with_proxy:
            self._autorun_list = self.config["minecraft"]["autorun"]
            self._autorun_proxy = self.config["minecraft"]["autorun_proxy"]
            if self._autorun_proxy:
                self.log.info("Auto-starting the proxy...")
        
            for serv_name in self._autorun_list:
                server = self.proxy.get_server(serv_name)
                if not server:
                    self.log.error(f"Server \"{server_name}\" not found. It is being ignored.")
                    continue
                else:
                    self.log.info("Auto-starting server \"{server_name}\"...")
                    server.start()
        else:
            if self.config["minecraft"]["server_autorun"]:
                self.log.info("Auto-starting the server ...")
                self.server.start()
        # ...
        
            

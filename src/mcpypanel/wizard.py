import sys
import os,time
import hashlib


global TEST_MODE
TEST_MODE = False
try:
    from .config import ConfFile
    from .control.console import Console
    from .__version__ import *
    from .exceptions import *
except ImportError:
    # For Testing
    TEST_MODE = True
    from config import ConfFile
    from control.console import Console
    from __version__ import *
    from exceptions import *

class DummyParent:
    def __init__(self):
        global BANNER,_BANNER_SIZE
        self.BANNER = BANNER
        self._BANNER_SIZE = _BANNER_SIZE
        self.config = dict()



    
    
    
class Wizard:
    def __init__(self,parent):
        self.parent = parent
        self.console = Console(self.parent,"Wizard")

    def _first_time_run(self):
        if not TEST_MODE:
            self.parent.config = ConfFile(self.parent,create=True)
        self.config = self.parent.config
        self.console._colored = False
        self.console._print_header()
        self.console._fancy_print("## McPyPanel Setup Wizard")
        self.console._fancy_print("It look like there is no configration in this directory.")
        d = self._check_aborting_from_input(self.console.ask_yes_no(f"Are you sure you want to setup an instance of McPyPanel in this directory ? (for Security purpose)"))

        if not d:
            d = self._check_aborting_from_input(self.console.ask_yes_no(f"Do you want to install McPyPanel in another directory ?"))
            if not d:
                self._abort_installation()
            path = self._check_aborting_from_input(self.console.ask_input(f"Enter the Full Path of the directory you want McPyPanel to install this instance in:"))



        
        d = self.console.ask_yes_no("Do you allow McPyPanel to use colours in the console ?")
        self._check_aborting_from_input(d)
        if d:
            self.console._colored = True
            self.console._print_header()
            self.console._fancy_print("Ho! look how better it is!")
        else:
            self.console._print_header()
            self.console._fancy_print("Haww... You're definitly missing something.")
        self.console._fancy_print("Let's get started!")
        
        #######################################
        self.consosle._fancy_print("At any time you can press Ctrl+C to abort the installation.")
        self.console._fancy_print("Everything that you set here can be changed in the app or by opening the file \"config.yaml\" (Not recomended)")
        self.console._fancy_print("Ask on the McPyPanel's discord server if you need anything.")
        time.sleep(1)
        ############Real Setup#################

        
        is_master = self._check_aborting_from_input(self.console.ask_input("Do you want to use this mcpypanel instance as a (1) master or a (2) slave ? ",default="1"))[0] == 1        
        self.config["is_master"] = is_master
        
        dashboard = self._check_aborting_from_input(self.console.ask_yes_no("Do you want to use the web-based interface (dashboard) ?"))
        self.config["allow_dashboard"] = dashboard
        remote = self._check_aborting_from_input(self.console.ask_yes_no("Do you allow this instance to be able to be remote controlled (Mainly GUI Client) ?"))
        self.config["allow_remote_control"] = dashboard


        
        while 1:
            password = self._check_aborting_from_input(self.console.ask_input("Enter the default password for the admin account"))
            if len(password) < 8:
                self.console._print_error("PasswordError","Password must be at least 8 char long.")
                continue
            retyped_password = self._check_aborting_from_input(self.console.ask_input("Please retype the password for the admin account"))
            if retyped_password == password:
                break
            self.console._print_error("PasswordError","The Passwords dosen't match")

        
        self.console._fancy_print("Valid password.")
        pass_hash = hashlib.md5(password).hexdigest() # Hash the password
        self.config["accounts"] = dict(admin=dict(perms="admin",password=pass_hash))
        
        
        
        
        
        
        #######################################      
        
        self.console._fancy_print("Alright, mcpypanel's setup in this directory is done! Enjoy!")
        self._abort_installation() # Testing


    def create_account(self,name,password,perms="guest"):
        self.config = self.parent.config
        if name in self.config["accounts"]:
            raise AccountAlreadyExistError("The Account %s already exist." % name)
        pass_hash = hashlib.md5(password.encode()).hexdigest()
        self.config["account"][name] = dict(perms=perms,password=pass_hash)

    def delete_account(self,name):
        self.config = self.parent.config
        if name not in self.config["accounts"]:
            raise AccountNotFoundError("The Account %s do not exist." % name)
        
    
    def _abort_installation(self):
        self.console._fancy_print("Aborting Installation.")
        sys.exit()

    def _check_aborting_from_input(self,inp):
        if inp is None:
            self._abort_installation()
        return inp

if TEST_MODE:
    w = Wizard(DummyParent())
    try:
        w._first_time_run()
    finally:
        time.sleep(3)
    

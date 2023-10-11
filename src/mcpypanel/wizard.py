import sys
from .config import ConfFile
from .control.console import Console
from .__version__ import *

class DummyParent:
    def __init__(self):
        global BANNER,_BANNER_SIZE
        self.BANNER = BANNER
        self._BANNER_SIZE = _BANNER_SIZE
    
    
    
    
class Wizard:
    def __init__(self,parent):
        self.parent = parent
        self.console = Console(self.parent,"Wizard")

    def _first_time_run(self):
        self.console._colored = False
        #self.console._print_header()
        self.console._fancy_print("## McPyPanel Setup Wizard")
        self.console._fancy_print("It look like there is no configration in this directory.")
        d = self.console.ask_yes_no(f"Are you sure you want to setup McPyPanel in this directory? (for Security purpose)")
        if not d:
            self._abort_installation()
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
        
        self.console._fancy_print("Alright, mcpypanel's setup in this directory is done! Enjoy!")
        self._abort_installation() # Testing
        
    def _abort_installation(self):
        self.console._fancy_print("Aborting Installation.")
        sys.exit()

    def _check_aborting_from_input(self,inp):
        if inp is None:
            self._abort_installation()

# if __name__ == "__main__":
# w = Wizard(DummyParent())
# w._first_time_run()
    

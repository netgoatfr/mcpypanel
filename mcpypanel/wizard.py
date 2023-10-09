import sys
from config import ConfFile
from control.console import Console

class Wizard:
    def __init__(self,parent):
        self.parent = parent
        self.console = Console(self,"Wizard")

    def _first_time_run(self):
        self.console._print("It look like there is no configration in this directory.")
        d = self.console.ask_yes_no("Are you sure you want to setup McPyPanel in this directory? (for Security purpose)")
        if not d:
            self.console._print("Aborting Setup.")
            sys.exit()
        while 1:pass


if __name__ == "__main__":
    w = Wizard(None)
    w._first_time_run()
    

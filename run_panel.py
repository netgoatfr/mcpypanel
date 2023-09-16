from mcpypanel import *

import sys

import os

class Panel:
    def __init__(self,args):
        self.log = Logger("Panel")
        self._BASE_DIR = os.path.split(args[0])[0]
        self._DIR = self._BASE_DIR + "mcpypanel_data"
        self._args = args

        self._first_time = False
        self.debug = False
        self._abort_startup = False
        self._return_code = 0
        
        if not os.path.exists(self._DIR) or not os.path.isdir(self._DIR) or not os.listdir(self._DIR):
            self._first_time = True
        else:
            self.config = ConfFile(self)
            if self._abort_startup:
                self._return_code = 1
                return
            if self.config["reset_panel"]
            self.debug = self.config["debug"]
            self.logger.colored_output = self.config["colored_output"]
    



def main(*args):
    panel = Panel(args)
    return panel._return_code or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[0]))

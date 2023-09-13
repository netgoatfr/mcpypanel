from mcpypanel import *

import sys

import os

class Panel:
	def __init__(self,args):
        self.log = logger.Logger("Panel")

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
            self.config = config.ConfFile(self)
            if self._abort_startup:
                self._return_code = 1
                return
            self.debug = self.config["debug"]
            self.logger("")



def main(*args):
	panel = Panel(args)
	return panel._return_code or 0


if __name__ == "__main__":
	sys.exit(main(sys.args))

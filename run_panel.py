from mcpypanel import *

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

        self._banner_size = (len("\__|     \__| \______/ \__|         \__|    \__|      \__|  \__|\__|  \__|\________|\________|") ,8)

        self._banner = """\033[35;1m$$\      $$\  $$$$$$\  $$$$$$$\ $$\     $$\ $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$\       
$$$\    $$$ |$$  __$$\ $$  __$$\\$$\   $$  |$$  __$$\ $$  __$$\ $$$\  $$ |$$  _____|$$ |      
$$$$\  $$$$ |$$ /  \__|$$ |  $$ |\$$\ $$  / $$ |  $$ |$$ /  $$ |$$$$\ $$ |$$ |      $$ |      
$$\$$\$$ $$ |$$ |      $$$$$$$  | \$$$$  /  $$$$$$$  |$$$$$$$$ |$$ $$\$$ |$$$$$\    $$ |      
$$ \$$$  $$ |$$ |      $$  ____/   \$$  /   $$  ____/ $$  __$$ |$$ \$$$$ |$$  __|   $$ |      
$$ |\$  /$$ |$$ |  $$\ $$ |         $$ |    $$ |      $$ |  $$ |$$ |\$$$ |$$ |      $$ |      
$$ | \_/ $$ |\$$$$$$  |$$ |         $$ |    $$ |      $$ |  $$ |$$ | \$$ |$$$$$$$$\ $$$$$$$$\ 
\__|     \__| \______/ \__|         \__|    \__|      \__|  \__|\__|  \__|\________|\________|
\033[0m"""
        
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

        #self._console_or_gui = self.config["use_gui"]

        self.run()

    def run():
        #if not self._console_or_gui
        print(self._banne)



def main(*args):
    panel = Panel(args)
    return panel._return_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[0]))

# import curses
# from curses.textpad import Textbox, rectangle
from colorama import Style, Fore, Back,init
import sys,os
from typing import *
init()
from colorama import just_fix_windows_console
just_fix_windows_console()



# Test of a console using curses

"""
class Console:
    def __init__(self,):
        ################################
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(1)
        ################################
        self._size = (curses.LINES,curses.COLS)
        self.windows = {"log":curses.newwin(curses.LINES,40, 0, 0)}
        self.current_window = "log"
        try:
            self.run()
        finally:    
            ################################
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            ################################
        
    def run(self):
        self._init()
        while 1:
            key = self.stdscr.getch()
            
            self.windows["log"].erase()
            self.windows["log"].insstr(1,2," "*18+"LOG "+" "*18)
            self.windows["log"].hline(2,2,"#",self.windows["log"].getmaxyx()[1]-1)
            if key != -1:
                self.windows["log"].insstr(chr(key))
            self.windows["log"].refresh()
            if key == ord("q"):
                break
            elif key in [curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT]:
                curses.beep()
                #self._handle_keys(key)
            \"""
            elif key == curses.KEY_RESIZE:
                curses.resize_term(*self.stdscr.getmaxyx())
                self.stdscr.clear()
                self._resize()
            \"""
            self.stdscr.refresh()
            
    def _init(self):
        y,x=self.windows["log"].getmaxyx()
        i,j=self.windows["log"].getparyx()
        rectangle(self.stdscr,i+1,j+1,y-1,x)
        
        self.windows["log"].insstr(1,1," "*18+"LOG "+" "*18)
        self.windows["log"].hline(2,1,"#",self.windows["log"].getmaxyx()[1]-1)
        
        self.windows["log"].refresh()
        self.stdscr.refresh()
        curses.doupdate()
                
    def write(self,text,window=None):
        \"""
        Write text to the current screen.
        
        Can be used as a waky solution, with print:
            print("Hello world",file=console)
        \"""
        if window is None:
            window = self.windows["log"]
"""   






class Console:
    USED_COLORS = [Style.RESET_ALL,Fore.LIGHTMAGENTA_EX,Fore.LIGHTBLUE_EX,Fore.LIGHTGREEN_EX,Fore.LIGHTRED_EX]
    def __init__(self,parent,master="Console"):
        self.parent = parent
        self._commands:dict[tuple[Callable,str]] = {}
        self._master = master
        self._colored = True
    
    def _handle_command(self,inp):
        cmd,*args = inp.split(" ")
        subcmds = []
        settings = []
        for a in args:
            if a.startswith("-"):
                settings.append(a)
            else:
                subcmds.append(a)
                
        if cmd not in self._commands:
            self._print_error("Command not found.","Syntax Error")
        _func = self._commands[cmd]
        return _func(subcmds = subcmds,settings = settings)
    
    def _register_command(self,func,command):
        self._commands[command] = func
        
    def _cmd_run(self):
        try:
            self._handle_command(self.ask_input("$"))
        except Exception as e:
            self._print_error(str(e.__class__.__name),e)
    
    def _print_header(self):
        if self._colored:print("\033[H\033[J",end="")
        self._print(Fore.LIGHTGREEN_EX+"#"*(self.parent._BANNER_SIZE()[0]+4))
        for i in range(1,self.parent._BANNER_SIZE()[1]+1):
            self._print(Fore.LIGHTGREEN_EX+"# "+Fore.LIGHTMAGENTA_EX+self.parent.BANNER.split("\n")[i]+Fore.LIGHTGREEN_EX+" #")
        self._print(Fore.LIGHTGREEN_EX+"#"*(self.parent._BANNER_SIZE()[0]+4))
            
    def _print(self,data):
        if self._colored:
            print(data+Style.RESET_ALL)
        else:
            for i in self.USED_COLORS:
                data = data.replace(i,"")
            print(data)
    def _fancy_print(self,data):
        self._print("["+self._master+"] "+Fore.LIGHTBLUE_EX+data)
    def _print_error(self,error_class="Error",error=""):
        error = Fore.LIGHTRED_EX+error_class+(": "+error) if error else ""
        self._print("["+self._master+"] "+error)
    
    def ask_input(self,prompt,default=None):
        if self._colored:
            prompt = "["+self._master+"] "+Fore.LIGHTBLUE_EX+prompt+Fore.LIGHTGREEN_EX+(" (default: "+str(default)+")" if default else "")
        else:
            prompt = "["+self._master+"] "+prompt+(" (default: "+str(default)+")" if default else "")
        try:
            return input(prompt+" > "+(Style.RESET_ALL if self._colored else "")) or default
        except KeyboardInterrupt:
            print()
            return None
        except:
            return None
    def ask_yes_no(self,prompt,default=True):
        if self._colored:
            prompt = "["+self._master+"] "+Fore.LIGHTBLUE_EX+prompt+Fore.LIGHTGREEN_EX+(" [Y/n]" if default else "[y/N]")
        else:
            prompt = "["+self._master+"] "+prompt+(" [Y/n]" if default else "[y/N]")
        try:
            data = input(prompt+" > "+(Style.RESET_ALL if self._colored else ""))
            if not data:return default
            return data.lower()[0] == "y"
        except KeyboardInterrupt:
            print()
            return None
        except:
            return None


class Commands:
    def __init__(self,parent):
        self.parent = parent
        for i in dir(self):
            if i.startswith("cmd"):
                self.parent.console._register_command(getattr(self,i))
        self.console = self.parent.console
    def  cmd_servers(self,sub,settings): # Sub is the sub commands
        if not sub: sub = ("list",)
        if sub[0] == "list":
            with_infos = "-i" in settings
            if self.parent._with_proxy:
                self.console._fancy_print("Here is a list of all the servers linked to this instance of mcpypanel:")
                for server in self.parent.proxy.servers:
                    self.console._fancy_print("  - "+server.name+(": running: "+("yes, " if server.running else "no, ")+"player count: "+str(len(server.players))) if with_infos else "")
            else:
                self.console._fancy_print("Here is the server linked to this instance of mcpypanel:")
                server = self.parent.server
                self.console._fancy_print("  - "+server.name+(": running: "+("yes, " if server.running else "no, ")+"player count: "+str(len(server.players))) if with_infos else "")
    def _print_subcmd_not_found(self,subcmd):
        self.console._print_error("Syntax Error",f"This subcommand ({subcmd}) was not found.")
        
if __name__ == "__main__":
    # For tests only
    def test():
        print("Hello")
    def test2(args):
        print("Hello",args)
    def _exit():
        exit()
    c = Console()
    c._print_header()
    c._register_command(test,"test")
    c._register_command(test2,"test2",["args"])
    c._register_command(_exit,"exit")
    while 1:
        c._cmd_run()
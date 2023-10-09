# import curses
# from curses.textpad import Textbox, rectangle
from colorama import Style, Fore, Back,init
import sys,os

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
    def __init__(self,parent,master="Console"):
        self.parent = parent
        self._commands = {}
        self._master = master
    
    def _handle_command(self,inp):
        cmd,*args = inp.split(" ")
        if cmd not in self._commands:
            self._print_error("Command not found.","Syntax Error")
        _func = self._commands[cmd][0]
        _f_args = self._commands[cmd][1]
        _args_list = []
        for i in _f_args:
            _args_list.append(eval(i))
        _func(*_args_list)
        
    def _cmd_run(self):
        self._handle_command(self.ask_input("$"))
    
    def _print_header(self):
        print("\033[H\033[J",end="")
        self._print(Fore.LIGHTGREEN_EX+"#"*(_BANNER_SIZE()[0]+4))
        for i in range(1,_BANNER_SIZE()[1]):
            self._print(Fore.LIGHTGREEN_EX+"# "+Fore.LIGHTMAGENTA_EX+BANNER.split("\n")[i]+Fore.LIGHTGREEN_EX+" #")
        self._print(Fore.LIGHTGREEN_EX+"#"*(_BANNER_SIZE()[0]+4))
            
    def _print(self,data):
        print(data+Style.RESET_ALL)
    def _fancy_print(self,data):
        self._print("["+self._master+"] "+Fore.LIGHTBLUE_EX+prompt)
    def _print_error(self,error,error_class = "Error"):
        error = Fore.LIGHTRED_EX+error_class+": "+error
        self._print(error)
    
    def ask_input(self,prompt,default=None):
        prompt = "["+self._master+"] "+Fore.LIGHTBLUE_EX+prompt+Fore.LIGHTGREEN_EX+(" (default: "+str(default)+")" if default else "")
        try:
            return input(prompt+" > "+Style.RESET_ALL)
        except KeyboardInterrupt:
            print()
            return None
        except:
            return None
    def ask_yes_no(self,prompt,default=True):
        prompt = "["+self._master+"] "+Fore.LIGHTBLUE_EX+prompt+Fore.LIGHTGREEN_EX+(" [Y/n]" if default else "[y/N]")
        try:
            data = input(prompt+" > "+Style.RESET_ALL)
            if not data:return default
            return data.lower()[0] == "y"
        except KeyboardInterrupt:
            print()
            return None
        except:
            return None
    def register_command(self,func,command,args=[]):
        self._commands[command] = (func,args)
            
            
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
    c.register_command(test,"test")
    c.register_command(test2,"test2",["args"])
    c.register_command(_exit,"exit")
    while 1:
        c._cmd_run()

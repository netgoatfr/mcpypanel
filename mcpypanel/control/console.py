# import curses
# from curses.textpad import Textbox, rectangle
import colorama
import sys,os

colorama.init()

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
    def __init__(self,parent):
        self.parent = parent
        self._commands = {}
        
    def register_command(self,func,command):
        self._commands[command] = func
            
            
if __name__ == "__main__":
    # For tests only
    c = Console()
    
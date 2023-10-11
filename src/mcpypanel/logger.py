"""
        Logging system
        credits to aGoatdev (github), me
        discord: netgoat
"""


from colorama import Fore, Back, Style, init
import sys
import time
import threading

init()

lock = threading.Lock()

TF_HOURS = "%H:%M:%S"
TF_DAYS = "%b %d %Y %H:%M:%S"
class Logger:
    def __init__(self,name,time_format = TF_HOURS,colored_output = True,file=sys.stdout):
        self.master = name
        self.lock = lock
        self.time_format = time_format
        self.colored_output = colored_output
        self.file=file
    def get_instance(self,child):
        return Logger(self.master+"#"+child,self.time_format,self.colored_output,file=self.file)
    def get_child(self,child):
        return Logger(self.master+"/"+child,self.time_format,self.colored_output,file=self.file)
    @property
    def _time(self):
        return time.strftime(self.time_format,time.gmtime(time.time()))
    
    def info(self,txt):
        self.lock.acquire()
        if self.colored_output:
            print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"["+self._time+"]"+" ["+self.master+"] [INFO]: "+txt+Style.RESET_ALL,file=self.file)
        else:
            print("["+self._time+"]"+" ["+self.master+"] [INFO]: "+txt,file=self.file)
        self.lock.release()
    def debug(self,txt):
        self.lock.acquire()
        if self.colored_output:print(Fore.LIGHTBLUE_EX+Style.BRIGHT+"["+self._time+"]"+" ["+self.master+"] [DEBUG]: "+txt+Style.RESET_ALL,file=self.file)
        else:print("["+self._time+"]"+" ["+self.master+"] [DEBUG]: "+txt,file=self.file)

        self.lock.release()
    def warning(self,txt):
        self.lock.acquire()
        if self.colored_output:print(Fore.YELLOW+Style.BRIGHT+"["+self._time+"]"+" ["+self.master+"] [WARN]: "+txt+Style.RESET_ALL,file=self.file)
        else:print("["+self._time+"]"+" ["+self.master+"] [WARN]: "+txt,file=self.file)

        self.lock.release()
    def error(self,txt):
        self.lock.acquire()
        if self.colored_output:print(Fore.LIGHTRED_EX+Style.BRIGHT+"["+self._time+"]"+" ["+self.master+"] [ERROR]: "+txt+Style.RESET_ALL,file=self.file)
        else:print("["+self._time+"]"+" ["+self.master+"] [ERROR]: "+txt,file=self.file)

        self.lock.release()
    def fatal(self,txt):
        self.lock.acquire()
        if self.colored_output:print(Fore.RED+Style.BRIGHT+"["+self._time+"]"+" ["+self.master+"] [FATAL]: "+txt+Style.RESET_ALL,file=self.file)
        else:print("["+self._time+"]"+" ["+self.master+"] [FATAL]: "+txt,file=self.file)

        self.lock.release()



if __name__ == '__main__':
    log1 = Logger("Test")
    log1.debug("Debug message")
    log1.info("Info message")
    log1.warning("Warning message")
    log1.error("Error message")
    log1.fatal("Critical message")
    log2 = log1.get_child("Child")
    log2.debug("Debug message")
    log2.info("Info message")
    log2.warning("Warning message")
    log2.error("Error message")
    log2.fatal("Critical message")
    log3 = log2.get_instance("Instance")
    log3.debug("Debug message")
    log3.info("Info message")
    log3.warning("Warning message")
    log3.error("Error message")
    log3.fatal("Critical message")
    log4 = log1.get_instance("Instance")
    log4.debug("Debug message")
    log4.info("Info message")
    log4.warning("Warning message")
    log4.error("Error message")
    log4.fatal("Critical message")
    


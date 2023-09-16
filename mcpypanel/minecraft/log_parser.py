import sys
import os,subprocess
import re
get_screen_id = lambda cmd: f"$(screen -ls | grep '[0-9]*\.{cmd}' | sed -E 's/\s+([0-9]+)\..*/\1/')"

class PaperStyle:
    

class LogWatcher:
  def __init__(self,file,parent):
    self.path = path
    self.parent = parent
    self._last_lines= []
  def refresh(self):
    try:
      with open(self.path) as f:
        lines = f.readlines() 
        for i in lines:
            if i not in self._last_lines:
                line = self.parse(i)
                if line is not None:
                    self.parent.events.trigger("minecraft.log.newline",line)
        except FileNotFoundError:
            return
    def parse(self,line):
        
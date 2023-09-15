import sys
import os,subprocess

get_screen_id = lambda cmd: f"$(screen -ls | grep '[0-9]*\.{cmd}' | sed -E 's/\s+([0-9]+)\..*/\1/')"


class LogWatcher:
  def __init__(self,file,parent):
    self.path = path
    self.parent = parent
    self.events = self.parents.events  
    self._last_content = None
  def refresh(self):
    try:
      with open(self.path) as f:
        if f.read() != self._last_content:
          self.events.trigger
      except FileNotFoundError:
        return
class ServerJar:
  def __init__(self,path,parent):
    self.parent = parent
    self.path = path
    self.log = self.parent.log.get_child("Minecraft")

    self._start = False
    self._running = False
    
    if not os.path.exists(self.path):
      self.log.error("Jar file not found, unable to start")
      return
    else:
      self._start = self.parent.log.ask_yes_no("Do you want to start the server now")
    if self._start

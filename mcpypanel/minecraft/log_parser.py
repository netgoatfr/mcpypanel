import sys
import os,subprocess
import re
import datetime
import uuid

#get_screen_id = lambda cmd: f"$(screen -ls | grep '[0-9]*\.{cmd}' | sed -E 's/\s+([0-9]+)\..*/\1/')"

class PaperStyle:
    base = re.compile("\[(\d\d)\:(\d\d)\:(\d\d)\] \[(.*)\/(.*)\]\: (.*)")
    uuid = re.compile("UUID of player (.*) is (.*)")
    logged_in = re.compile("(.*)\[/(.*):(.*)\] logged in with entity id (.*) at \(\[(.*)\](.*), (.*), (.*)\)")
    
class LogLineTypes:
	NORMAL = "normal"
	UUID_REGISTER = "uuid_register"
	USER_LOGGED = "user_logged"

	
class LogLevelType:
	DEBUG = "debug"
	INFO = "info"
	WARNING = "warning"
	ERROR = "error"
	CRITICAL = "critical"
	def get(i):
		if hasattr(LogLevelType,i.upper()):
			return getattr(LogLevelType,i.upper())
	

class DummyLogger:
	def info(*a):pass
	def warn(*a):pass
	def error(*a):pass
	def debug(*a):pass
	def fatal(*a):pass
	def get_child(self,*a):return self
class DummyParent:
	def __init__(self):
		self.log = DummyLogger()
		self.config = {}



class Line:
	def __init__(self,**kwargs):
		self.__dict__ = kwargs
	def __str__(self):
		return str(self.__dict__)

class LogWatcher:
	def __init__(self,path,parent):
		self.path = path
		self.parent = parent
		self.log = self.parent.log.get_child("LogWatcher")
		if self.parent.config.get("server_log_style","paper") == "paper":
			self.style = PaperStyle
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
	def parse(self,raw):
		line = self.style.base.match(raw)
		if not line:
			self.log.fatal("It's look like the log style is misconfigured, or this style dosen't exsist currently.")
			return
		datas = dict(raw=line.group(0))
		datas["time"] = datetime.time(int(line.group(1)),int(line.group(2)),int(line.group(3)))
		datas["worker"] = line.group(4)
		datas["log_level"] = LogLevelType.get(line.group(5))
		message = line.group(6)
		if (match := self.style.uuid.match(message)) is not None:
			datas["user_authenticator_thread"] = int(datas["worker"].split("#")[1])
			datas["player"] = match.group(1)
			datas["uuid"] = uuid.UUID(match.group(2))
			datas["type"] = LogLineTypes.UUID_REGISTER

		elif (match := self.style.logged_in.match(message)) is not None:
			datas["player"] = match.group(1)
			datas["ip"] = match.group(2)
			datas["port"] = int(match.group(3))
			datas["entity_id"] = int(match.group(4))
			datas["spawn_world"] = match.group(5)
			datas["spawn_x"] = float(match.group(6))
			datas["spawn_y"] = float(match.group(7))
			datas["spawn_z"] = float(match.group(8))
			datas["type"] = LogLineTypes.USER_LOGGED
			
		else:
			datas["message"] = message
			datas["type"] = LogLineTypes.NORMAL
		return Line(**datas)


l = LogWatcher("",DummyParent())
print(l.parse("[21:55:04] [Server thread/INFO]: captain_corazon[/81.220.113.89:42141] logged in with entity id 180 at ([world]-159.48689069165525, 68.0, 265.8047789565888)"))

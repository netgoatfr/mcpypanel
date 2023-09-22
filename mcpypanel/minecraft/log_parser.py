import sys
import os,subprocess
import re
import datetime
#get_screen_id = lambda cmd: f"$(screen -ls | grep '[0-9]*\.{cmd}' | sed -E 's/\s+([0-9]+)\..*/\1/')"

class PaperStyle:
    base = re.compile("\[(\d\d)\:(\d\d)\:(\d\d)\] \[(.*)\/(.*)\]\: (.*)")

class LogLineTypes:
	NORMAL = "normal"
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
			print("error")
		datas = dict(raw=line.group(0))
		datas["time"] = datetime.time(int(line.group(1)),int(line.group(2)),int(line.group(3)))
		datas["worker"] = line.group(4)
		datas["log_level"] = LogLevelType.get(line.group(5))

		if self.style..match(
		else:
			datas["message"]=line.group(6)
		
		return datas

l = LogWatcher("",DummyParent())
print(l.parse("[17:32:50] [ServerThread/INFO]: gg"))

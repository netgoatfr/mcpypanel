import sys
from .config import ConfFile


class Wizard:
	def __init__(self,parent):
		self.parent = parent

	def _ask_yes_no(self,prompt,default_yes=True):
		try:
			data = input(prompt+" [Y/n]  :" if default_yes else " [N/y]  :")
		except:return None
		if not data:return default_yes
		return data[0].lower() == "y"

	def run(self):
		print("#"*self.parent._banner_size[0])
		print(self.parent._banner)
		print("#"*self.parent._banner_size[0])
		print()
		print("It look like there is no configration in this directory.")
		d = self._ask_yes_no("Are you sure you want to setup McPyPanel in this directory? (for Security purpose)")
		if not d:
			print("\nAborting Setup.")
		while 1:pass

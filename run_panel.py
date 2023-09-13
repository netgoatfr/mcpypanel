from mcpypanel import *

import sys

class Panel:
	def __init__(self,args):pass;pass


def main(*args):
	panel = Panel(args)
	panel.run()
	return panel._return_code or 0


if __name__ == "__main__":
	sys.exit(main(sys.args))

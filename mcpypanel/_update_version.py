""" 
This is random junk, just here to help me track of the version as i intensly test mcpypanel.
Don't mind it.
"""
from __version__ import VERSION
data = open("mcpypanel/__version__.py").read()
lines = data.split("\n")
VERSION = list(VERSION)
for i,v in enumerate(VERSION[1:]):
    i += 1
    if v == 19:
        VERSION[i] = 0
        VERSION[i-1] += 1
        continue
    if i == len(VERSION)-1:
        VERSION[i] += 1
lines[0] = "VERSION = "+str(tuple(VERSION))
with open("mcpypanel/__version__.py","w") as f:
    for line in lines:
        f.write(line + "\n")
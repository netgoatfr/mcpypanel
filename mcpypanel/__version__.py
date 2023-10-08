VERSION = (0, 0, 1)
TYPE = "alpha"

__version__ = '.'.join(map(str, VERSION))
__version__ += TYPE

BANNER =""" _  _   ___  ____  _  _  ____   __   __ _  ____  __   
( \/ ) / __)(  _ \( \/ )(  _ \ / _\ (  ( \(  __)(  )  
/ \/ \( (__  ) __/ )  /  ) __//    \/    / ) _) / (_/\
\_)(_/ \___)(__)  (__/  (__)  \_/\_/\_)__)(____)\____/
"""
def _BANNER_SIZE():
    max = ""
    for i in BANNER.split("\n"):
        if len(i) > len(max):max = i
    return (len(max),len(BANNER.split("\n")))
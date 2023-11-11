VERSION = (0, 0, 1)
TYPE = "alpha"

__version__ = '.'.join(map(str, VERSION))
__version__ += TYPE

BANNER = r"""
 _  _   ___  ____  _  _  ____   __   __ _  ____  __   
( \/ ) / __)(  _ \( \/ )(  _ \ / _\ (  ( \(  __)(  )  
/ \/ \( (__  ) __/ )  /  ) __//    \/    / ) _) / (_/\
\_)(_/ \___)(__)  (__/  (__)  \_/\_/\_)__)(____)\____/"""

_BANNER_SIZE = (len(max(BANNER.split("\n"))),len([x for x in BANNER.split("\n") if x != ""]))
__all__ = dir()

if __name__ == "__main__":
    import time
    print(BANNER)
    print(_BANNER_SIZE)
    print("Current version "+__version__)
    time.sleep(5)

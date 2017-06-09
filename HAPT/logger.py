from config import *

def log(msg,mode=None):
    if mode is not None:
        print("\n" + msg + "\n") if debugMode == mode else None

    else:
        print("\n" + msg + "\n")

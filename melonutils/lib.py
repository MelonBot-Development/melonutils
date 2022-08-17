from os.path import abspath
from posixpath import dirname

if __name__ == "__main__":
    import melonutils
    
    path = dirname(abspath(melonutils.__file__)) + "/core"

from enum import Enum

class OpType(Enum):
    Set = 0
    Delete = 1
    Insert = 2
    Undo = 3
    Dummy = -1 # for testing purposes only
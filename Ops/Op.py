from abc import ABC, abstractmethod


class Op(ABC):
    def __init__(self, opType, id, value):
        self.id = id
        self.opType = opType
        self.value = value

    @abstractmethod
    def apply(self, state):
        pass

    @abstractmethod
    def undo(self, state):
        pass

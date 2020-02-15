from abc import ABC, abstractmethod
from Ops.OpType import OpType
from VectorClock import VectorClock


class Op(ABC):
    def __init__(self, opType: OpType, id: VectorClock, field: str, value):
        self.id = id
        self.opType = opType
        self.field = field
        self.value = value

    @abstractmethod
    def apply(self, state):
        pass

    @abstractmethod
    def undo(self, state):
        pass

    @abstractmethod
    def from_proto(self, proto):
        pass

    @abstractmethod
    def to_proto(self):
        pass
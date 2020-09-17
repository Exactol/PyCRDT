from abc import ABC, abstractmethod
from Ops.OpType import OpType
from VectorClock import VectorClock
from typing import Any

class Op(ABC):
    "Base Abstract Class for Operations"
    def __init__(self, field: str, value: Any, opType: OpType, id: VectorClock):
        self.field = field
        self.value = value
        self.id = id
        self.opType = opType

    @abstractmethod
    def apply(self, state):
        pass

    @abstractmethod
    def undo(self, state):
        pass

from abc import ABC, abstractmethod
from Ops.OpType import OpType
from Causality.VectorClockEntry import VectorClockEntry
from typing import Any

class Op(ABC):
    "Base Abstract Class for Operations"
    def __init__(self, field: str, value: Any, opType: OpType, clock_entry: VectorClockEntry):
        self.field = field
        self.value = value
        self.clock_entry = clock_entry
        self.opType = opType
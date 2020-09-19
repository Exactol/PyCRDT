from Ops.Op import Op
from Ops.OpType import OpType
from Causality.VectorClockEntry import VectorClockEntry
from Causality.VectorClock import VectorClock
from typing import Any, Dict
from CRDT.CRDTEntry import CRDTEntry

class SetOp(Op):
  """
  Sets the value of a field
  """
  def __init__(self, field: str, value: Any, clock_entry: VectorClockEntry):
    super().__init__(field, value, OpType.Set, clock_entry)
    # self.previous = None
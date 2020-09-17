from Ops.Op import Op
from Ops.OpType import OpType
from VectorClock import VectorClock
from typing import Any

class DeleteOp(Op):
  """
  Deletes a field. Doesn't actually delete, only tombstones
  """
  def __init__(self, field: str, value: Any, id: VectorClock):
    super().__init__(field, value, OpType.Delete, id)
    self.previous = None

  def apply(self, state: dict):
    if self.field in state:
      self.previous = state[self.field]
    # state[self.field] =

  def undo(self, state):
    state[self.field] = self.previous

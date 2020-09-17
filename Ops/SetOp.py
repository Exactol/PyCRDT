from Ops.Op import Op
from Ops.OpType import OpType
from VectorClock import VectorClock
from typing import Any

class SetOp(Op):
  """
  Sets the value of a field. Not commutative, but will converge using Last-Write-Wins
  """
  def __init__(self, field: str, value: Any, id: VectorClock):
    super().__init__(field, value, OpType.Set, id)
    # super().__init__(OpType.Set, id, field, value)
    self.previous = None

  def apply(self, state: dict):
    if self.field in state:
      self.previous = state[self.field]

    state[self.field] = (self.id, self.value)
    return state

  def undo(self, state):
    # TODO: if previous is null, field didnt previously exist and should be tombstoned
    state[self.field] = self.previous

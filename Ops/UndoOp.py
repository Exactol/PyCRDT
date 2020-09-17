
from .Op import Op
from .OpType import OpType
from VectorClock import VectorClock
from typing import Any

# TODO:
class UndoOp(Op):
  """
  Sets the value of a field
  """
  def __init__(self, id: VectorClock, field: str, value: Any):
    super().__init__(OpType.Add, id, field, value)

  def apply(self, state: dict):
    state[self.field] = (self.id, self.value)
    return state

  def undo(self, state):
    pass

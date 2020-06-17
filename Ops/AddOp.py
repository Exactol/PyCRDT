from .Op import Op
from .OpType import OpType

class AddOp(Op):
  """
  Sets the value of a field
  """
  def __init__(self, id, field: str, value):
    super().__init__(OpType.Add, id, field, value)

  def apply(self, state: dict):
    state[self.field] = (id, self.value)
    return state

  def undo(self, state):
    pass

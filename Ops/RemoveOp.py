from .Op import Op
from .OpType import OpType

class RemoveOp(Op):
  """
  Removes a field
  """
  def __init__(self, id, field: str, value):
    super().__init__(OpType.Remove, id, field, value)

  def apply(self, state: dict):
    pass

  def undo(self, state):
    pass

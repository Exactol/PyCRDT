from Ops.Op import Op
from Ops.OpType import OpType


class AddOp(Op):
  def __init__(self, id, field: str, value):
    super(AddOp, self).__init__(OpType.Add, id, field, value)

  def apply(self, state: dict):
    state[self.field] = (id, self.value)
    return state

  def undo(self, state):
    pass

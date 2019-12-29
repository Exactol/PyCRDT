from Ops.Op import Op
from Ops.OpType import OpType


class AddOp(Op):
  def __init__(self, id, value):
    super(OpType.Add, id, value)

  def apply(self, state):
    pass

  def undo(self, state):
    pass

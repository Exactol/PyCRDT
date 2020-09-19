from Ops.Op import Op
from Ops.OpType import OpType
from Causality.VectorClockEntry import VectorClockEntry

class DummyOp(Op):
  """
  DO NOT USE: Exists only for testing Unsupported Operations
  """
  def __init__(self):
    super().__init__(None, None, OpType.Dummy, VectorClockEntry("dummy"))
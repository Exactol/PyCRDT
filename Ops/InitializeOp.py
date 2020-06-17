from Ops import Op, OpType
from VectorClock import VectorClock

class InitializeOp(Op):
  """
  A noop op that signals the remote CRDT store to perform initial handshake
  """
  def __init__(self):
    super().__init__(OpType.Initialize, VectorClock(0), "", None)

  def apply(self, state: dict):
    return state

  def undo(self, state):
    return state

from CRDT.CRDTStore import CRDTStore
from Ops import SetOp, DeleteOp
from VectorClock import VectorClock
from typing import Dict, Any
from Callback import Callback

class CRDT:
  """
  TODO:
  """
  def __init__(self, user_id = 0, initial_version: Dict[int, int] = None, initial_state: Dict[str, Any] = {}):
    # setup correct initial state
    initial_state = {k: (VectorClock(user_id), v) for k, v in initial_state.items()}

    self.store = CRDTStore(user_id, initial_version, initial_state)

    # forward callbacks from base store to listeners
    self.on_update = self.store.on_update

  def set(self, field, value):
    next_version = self.store.version.increment()
    op = SetOp(field, value, next_version)
    self.store.apply(op)

  def get(self, field):
    return self.store.get(field)

  # def delete(self, field):
  #   next_version = self.store.version.increment()
  #   op = DeleteOp()
  #   self.store.apply(op)
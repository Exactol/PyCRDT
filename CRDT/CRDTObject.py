from CRDT.Map import Map
from Ops import SetOp, DeleteOp
from Causality.VectorClock import VectorClock
from typing import Dict, Any
from Callback import Callback

class CRDT:
  """
  TODO:
  """
  def __init__(self, user_id = 0, initial_version: Dict[int, int] = None, initial_state: Dict[str, Any] = {}):
    # setup correct initial state
    initial_state = {k: (VectorClock(user_id), v) for k, v in initial_state.items()}

    self.user_id = user_id
    self.store = Map(initial_version, initial_state)

    # forward callbacks from base store to listeners
    self.on_update = self.store.on_update

  def set(self, field, value):
    """
    Generates a Set operation and applies it to the backing CRDT store
    """
    next_version = self.store.clock().increment(self.user_id)
    op = SetOp(field, value, next_version)
    self.store.apply(op)

  def get(self, field):
    return self.store.get(field)

  # def delete(self, field):
  #   next_version = self.store.version.increment()
  #   op = DeleteOp()
  #   self.store.apply(op)
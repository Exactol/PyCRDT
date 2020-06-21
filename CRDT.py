from CRDTStore import CRDTStore
from Ops import AddOp
from typing import Dict, Any

class CRDT():
  def __init__(self, user_id = 0, initial_version: Dict[int, int] = None, initial_state: Dict[str, Any] = {}):
    self.store = CRDTStore(user_id, initial_version, initial_state)
    self.on_update = self.store.on_update

  def set(self, field, value):
    next_version = self.store.version.increment()
    op = AddOp(next_version, field, value)
    self.store.apply(op)

  def get(self, field):
    return self.store.get(field)

  # TODO:
  def delete(self, field):
    pass
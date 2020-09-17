from VectorClock import VectorClock
from History import History
from Ops import SetOp, Op, OpType
from json import loads
from Callback import Callback
from typing import Dict, Any, Tuple
from collections import namedtuple
from CRDT.CRDTEntry import CRDTEntry

class CRDTStore:
  """
  Handles the state management of the CRDT store.
  """
  def __init__(self, user_id = 0, initial_version: Dict[int, int] = None, initial_state: Dict[str, CRDTEntry] = {}):
    self.state: Dict[str, CRDTEntry] = initial_state
    self.initial_state: Dict[str, Tuple[VectorClock, Any]] = initial_state
    self.history: History = History()

    self.user_id: int = user_id
    self.version: VectorClock = VectorClock(user_id, initial_version)

    self.on_update: Callback = Callback()

  def apply(self, op: Op):
    # TODO: ignore duplicates?

    # update version
    self.version.merge(op.id)

    # apply and store history
    self.state = op.apply(self.state)
    self.history.append(op)

    self.on_update()

  def get(self, field: str):
    if field in self.state:
      return self.state[field].value # TODO: check if tombstoned

    return None
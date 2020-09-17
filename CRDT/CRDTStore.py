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
  Acts as a map CmRDT
  """
  def __init__(self, initial_version: Dict[Any, int] = None, initial_state: Dict[str, CRDTEntry] = {}):
    self.state: Dict[str, CRDTEntry] = initial_state
    self.initial_state: Dict[str, CRDTEntry] = initial_state

    # TODO: make history a global provider
    self.history: History = History()

    # this clock is the current version of the CRDTStore and should be greater or equal to all entry clock values
    self.clock: VectorClock = VectorClock(initial_version)

    self.on_update: Callback = Callback()

  def apply(self, op: Op):
    """
    Applies an operation to the CRDTStore
    """
    # update version
    # self.version.merge(op.id)

    # apply and store history
    self.state = op.apply(self.state, self.clock)
    # self.history.append(op)

    self.on_update()

  def get(self, field: str):
    """
    Returns a field. Defaults to None if the field doesn't exist
    """
    # TODO: check if tombstoned?
    return self.state.get(field, None)

  def keys(self):
    pass
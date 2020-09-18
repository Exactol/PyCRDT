from VectorClock import VectorClock
from History import History
from Ops import SetOp, Op, OpType
from json import loads
from Callback import Callback
from typing import Dict, Any, Tuple
from collections import namedtuple
from CRDT.CRDTEntry import CRDTEntry
from CRDT.CmRDT import CmRDT

class Map(CmRDT):
  """
  Map CRDT

  Compositions of CRDTS are themselves CRDTS. This means that the map can hold values that are CRDTs
  """
  def __init__(self, initial_clock: VectorClock = VectorClock(), initial_state: Dict[str, CRDTEntry] = {}):
    self.state: Dict[str, CRDTEntry] = initial_state.copy()
    self.initial_state: Dict[str, CRDTEntry] = initial_state.copy()

    # TODO: make history a global provider
    self.history: History = History()

    # this clock is the current version of the CRDTStore and should be greater or equal to all entry clock values
    self.clock: VectorClock = initial_clock.copy()

    self.on_update: Callback = Callback()

  def apply(self, op: Op):
    """
    Applies an operation to the Map
    """
    # apply and store history
    op.apply(self.state, self.clock)
    # self.history.append(op)

    self.on_update()

  def get(self, field: str):
    """
    Returns a field. Defaults to None if the field doesn't exist
    """
    # TODO: check if tombstoned?
    # TODO: should this return a default CRDTEntry instead of None?
    return self.state.get(field, None)

  def keys(self):
    pass
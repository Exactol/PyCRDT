from CRDT.CmRDT import CmRDT
from CRDT.CRDTEntry import CRDTEntry
from VectorClock import VectorClock
from typing import Dict, Any
from Callback import Callback
from Ops.Op import Op
from Ops.SetOp import SetOp

class LWWRegister(CmRDT):
  """
  Last-Writer-Wins Register CRDT

  Holds an arbitrary value. The value is updated according to the timestamp of the Op
  """
  def __init__(self, initial_state: CRDTEntry = CRDTEntry(None)):
    self.state = initial_state.copy()
    self.on_update: Callback = Callback()
    # TODO: does this need initial_state?

  def apply(self, op: Op):
    """
    Applies an operation to the LWWRegister.
    """
    # TODO: handle concurrent clocks. Ex. <1, 2>, <2, 1> Updates happen concurrently, need some kind of tie breaker. maybe assign user ids based on order joined or assign users priority?
    # TODO: should lww have a delete op?
    # TODO: implement undo op
    if isinstance(op, SetOp):
      # update the register if this operation has a newer clock
      if self.state.clock.get(op.clock_entry.identifier) < op.clock_entry.counter:
        self.state = CRDTEntry(op.value, self.state.clock.apply(op.clock_entry))
      # if clocks are equal but the value differs something went wrong
      elif self.state.clock.get(op.clock_entry.identifier) == op.clock_entry.counter and self.state.value != op.value:
        raise Exception("Conflicting clocks")
      else:
        # op has older clock version, do nothing
        return
    else:
      raise Exception("Unsupported operation")

    self.on_update()

  def get(self):
    """
    Returns the value of the register.
    """
    # TODO: check if tombstoned?
    return self.state.value

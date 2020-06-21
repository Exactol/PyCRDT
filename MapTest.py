import asyncio
from functools import reduce

from RemoteCRDTStore import RemoteCRDTStore
from Ops.AddOp import AddOp
from Server import ThreadedClient
from CRDT import CRDT


class MapTest:
  def __init__(self, server):
    self.state = CRDT()
    self.state.on_update += lambda: self.print()

  def set(self, field, value):
    self.state.set(field, value)

  def print(self):
    print(self.state.store.state)
    print(" -> ".join(map(lambda x: str(x.id), self.state.store.history)))
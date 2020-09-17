import asyncio
from functools import reduce

from ServerProviders import ThreadedSocketClient
from CRDT import CRDT, RemoteCRDTStore


class MapTest:
  def __init__(self, server):
    self.state = CRDT()
    self.state.on_update += lambda: print(self)

  def set(self, field, value):
    self.state.set(field, value)

  def delete(self, field):
    # self.state.delete(field)
    pass

  def __str__(self):
    return f"""State: {self.state.store.state}
Version: {self.state.store.clock}"""
# {" -> ".join(map(lambda x: str(x.id), self.state.store.history))}"""
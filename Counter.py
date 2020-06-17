import asyncio
from functools import reduce

from RemoteCRDTStore import RemoteCRDTStore
from Ops.AddOp import AddOp
from Server import ThreadedClient


class Counter:
    def __init__(self, server):
        self.state = RemoteCRDTStore(server, 1 if isinstance(server, ThreadedClient) else 0)
        self.state.on_update += lambda: self.print()

    def increment(self):
        v = self.state.get("a")
        if v is None:
            v = 0
        newVersion = self.state.version.increment()
        op = AddOp(newVersion, "a", v + 1)
        self.state.apply(op)

    def print(self):
        print(self.state.get("a"))
        print(" -> ".join(map(lambda x: str(x.id), self.state.history)))
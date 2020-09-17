import asyncio
from functools import reduce

from ServerProviders import ThreadedSocketClient
from CRDT import CRDT, RemoteCRDTStore


class Counter:
    def __init__(self, server):
        # self.state = RemoteCRDTStore(server, 1 if isinstance(server, ThreadedClient) else 0)
        self.state = CRDT()
        self.state.on_update += lambda: self.print()

    def increment(self):
        a = self.state.get("a")
        if a is None:
            a = 0
        self.state.set("a", a + 1)

    def print(self):
        print(self.state.get("a"))
        print(" -> ".join(map(lambda x: str(x.id), self.state.store.history)))
import asyncio
from functools import reduce

from CRDTStore import CRDTStore
from Ops.AddOp import AddOp


class Counter:
    def __init__(self, server):
        self.state = CRDTStore(server)

    def increment(self):
        newId = self.state.create_id()
        op = AddOp(newId, 1)
        self.state.apply(op)

    def get_count(self):
        total = 0
        for _, v in self.state.state.items():
            total += v
        return total
from functools import reduce
from Store import Store
import asyncio

class Counter:
    def __init__(self):
        self.state = Store()
        loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=loop)

    def increment(self):
        self.state.add(1)

    def get_count(self):
        total = 0
        for k, v in self.state.state.items():
            total += v
        return total
        # return reduce(lambda x: x, self.state.state.values())

    async def client(self):
        pass

    async def server(self):
        pass

    def start_server(self):
        pass

    def start_client(self):
        pass
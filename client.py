import asyncio
from singleton import Singleton

class Client(metaclass=Singleton):
    def __init__(self, queue, reader, loop):
        self.queue = queue
        self.reader = reader
        asyncio.run_coroutine_threadsafe(self.run_client(), loop)

    async def run_client(self):
        while True:
            data = await self.reader.read(100)
            # print(data.decode())
            if not data:
                break
            await self.queue.put(data.decode())
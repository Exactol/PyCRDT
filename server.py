import asyncio
from singleton import Singleton

class Server(metaclass=Singleton):
    def __init__(self, queue, writer, loop):
        self.queue = queue
        self.writer = writer
        asyncio.run_coroutine_threadsafe(self.run_server(), loop)

    async def run_server(self):
        while True:
            data = await self.queue.get()
            if not data:
                break
            print(data)
            self.writer.write(data.encode())

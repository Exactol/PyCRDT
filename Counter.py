from functools import reduce
from Store import Store
import asyncio
import websockets

class Counter:
    def __init__(self):
        self.state = Store()

    def increment(self):
        self.state.add(1)

    def get_count(self):
        total = 0
        for k, v in self.state.state.items():
            total += v
        return total
        # return reduce(lambda x: x, self.state.state.values())

    async def tcp_server(self, reader, writer):
        data = await reader.read()
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f'Recieved data from {addr}')
        print(message)

    async def start(self):
        async with self.server:
            await self.server.serve_forever()

    async def server_main(self):
        self.server = await asyncio.start_server(self.tcp_server, 'localhost', 1480, )

        addr = self.server.sockets[0].getsockname()
        print(f'Serving on port {addr}')

        await asyncio.create_task(self.server.serve_forever())
        # async with self.server:
        # self.server.serve_forever()

        # self.server.

    def start_server(self):
        asyncio.run(self.server_main())

    def stop_server(self):
        self.server.close()

    async def tcp_client(self):
        self.reader, self.writer = await asyncio.open_connection('localhost', 1480)

    def start_client(self):
        asyncio.run(self.tcp_client())

    def stop_client(self):
        self.reader.close()
        self.writer.close()
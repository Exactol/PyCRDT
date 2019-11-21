import asyncio

async def tcp_server(reader, writer):
    data = await reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f'Recieved data from {addr}')
    print(message)

async def main():
    server = await asyncio.start_server(tcp_server, 'localhost', 1480)

    addr = server.sockets[0].getsockname()
    print(f'Serving on port {addr}')

    async with server:
        await server.serve_forever()

def start():
    asyncio.run(main())
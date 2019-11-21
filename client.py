import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('localhost', 1480)
    writer.write('test\0'.encode())
    writer.close()


async def start():
    asyncio.run(tcp_client())
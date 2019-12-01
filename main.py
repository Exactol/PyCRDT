import asyncio
import sys
from client import Client
from server import Server
from Counter import Counter
from threading import Thread

async def server_callback(reader, writer):
    print("Connection recieved")
    loop = asyncio.get_running_loop()
    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    c = Client(in_queue, reader, loop)
    s = Server(out_queue, writer, loop)

    while True:
        d = await in_queue.get()
        print("Recieved: ")
        print(d)
        if not d:
            break

async def server_main(loop):
    print("Starting server")
    server = await asyncio.start_server(server_callback, 'localhost', 1480, loop=loop)
    async with server:
        await server.serve_forever()

async def client_main(loop):
    print("Starting client")
    reader, writer = await asyncio.open_connection('localhost', 1480)
    await server_callback(reader, writer)

async def start_server(loop):
    print("Starting server")
    asyncio.run(server_main(loop))

async def start_client(loop):
    print("Starting client")
    asyncio.run(client_main(loop))

if __name__ == "__main__":
    # counter = Counter()
    server_mode = sys.argv[1] == "--server"
    new_loop = asyncio.new_event_loop()
    # thread = None
    # if server_mode:
    thread = Thread(target=start_server, args=new_loop)
    thread.start()
    # else:
    #     asyncio.run(client_main())

    print("On bg")
    while thread.is_alive():
        pass
    # print("Press Q to exit")
    # while inp := input() != 'q':
    #     counter.increment()
    #     print(f'Counter value: {counter.get_count()}')

    # if server_mode:
    #     counter.stop_server()
    # else:
    #     counter.stop_client()
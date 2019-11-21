import asyncio
import sys
import server
import client
from Counter import Counter

if __name__ == "__main__":
    counter = Counter()
    server_mode = sys.argv[1] == "--server"

    if server_mode:
        print("Starting server")
        counter.start_server()
    else:
        print("Starting client")
        counter.start_client()

    print("Press Q to exit")
    while inp := input() != 'q':
        counter.increment()
        print(f'Counter value: {counter.get_count()}')

    if server_mode:
        counter.stop_server()
    else:
        counter.stop_client()
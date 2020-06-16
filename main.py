import asyncio
import functools
import sys
from threading import Event, Thread
from typing import Union

from Counter import Counter
from VectorClock import VectorClock
from ThreadedClient import ThreadedClient
from ThreadedServer import ThreadedServer
from Ops.AddOp import AddOp
from json import dumps, loads
from JsonUtils import CRDTDecoder, CRDTEncoder

if __name__ == "__main__":

    server_mode = sys.argv[1] == "--server"

    # server: Union[ ThreadedServer, ThreadedClient ] = None
    # if (server_mode):
    #     print("Starting server")
    #     server = ThreadedServer('localhost', 1480)
    # else:
    #     print("Starting client")
    #     server = ThreadedClient('localhost', 1480)

    # server.start()
    # counter = Counter(server)

    # while True:
    #     inp = input("Press z to exit\n")
    #     if (inp == "z" or inp == "Z"):
    #         break
    #     else:
    #         counter.increment()
    # server.stop()


    version = VectorClock(0)
    op = AddOp(version, "a", 1)
    str_op = dumps(op, cls=CRDTEncoder)
    print(str_op)
    obj = loads(str_op, cls=CRDTDecoder)
    print(obj)

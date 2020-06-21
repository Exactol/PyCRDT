import asyncio
import functools
import sys
from threading import Event, Thread
from typing import Union

from Counter import Counter
from VectorClock import VectorClock
from Server import ThreadedClient, ThreadedServer, ServerBase
from Ops.AddOp import AddOp
from json import dumps, loads
from JsonUtils import CRDTDecoder, CRDTEncoder
from MapTest import MapTest

if __name__ == "__main__":
  server_mode = sys.argv[1] == "--server"

  server: ServerBase = None
  if (server_mode):
    print("Starting server")
    server = ThreadedServer('localhost', 1480)
  else:
    print("Starting client")
    server = ThreadedClient('localhost', 1480)

  server.start()
  mapTest = MapTest(server)

  # counter testing
  # counter = Counter(server)
  # while True:
  #     inp = input("Type z to exit\n")
  #     if (inp == "z" or inp == "Z"):
  #         break
  #     else:
  #         counter.increment()

  # map testing
  while True:
    inp = input("Enter field,value. Type z to exit\n")
    if (inp == "z" or inp == "Z"):
      break
    else:
      try:
        field,value = inp.split(",")
        mapTest.set(field, value)
      except:
        pass
  server.stop()
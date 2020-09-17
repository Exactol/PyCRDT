import asyncio
import functools
import sys
from threading import Event, Thread
from typing import Union

from Counter import Counter
from VectorClock import VectorClock
from ServerProviders import ThreadedSocketClient, ThreadedSocketServer, ThreadedSocketBase
from MapTest import MapTest

if __name__ == "__main__":
  server_mode = sys.argv[1] == "--server"

  server: ThreadedSocketBase = None
  if (server_mode):
    print("Starting server")
    server = ThreadedSocketServer('localhost', 1480)
  else:
    print("Starting client")
    server = ThreadedSocketClient('localhost', 1480)

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
    inp = input("To Add: field,value. To Delete: delete field. To Undo: undo field. Type z to exit\n")
    if (inp == "z" or inp == "Z"):
      break
    elif inp.startswith("delete"):
      command,field = inp.split(" ")
      try:
        mapTest.delete(field)
      except:
        print("failed to delete")
    elif inp.startswith("undo"):
      pass
    else:
      try:
        field,value = inp.split(",")
        mapTest.set(field, value)
      except:
        print("failed to set")
    # spacing
    print()
  server.stop()
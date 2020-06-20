from abc import ABC, abstractmethod
from queue import Empty, Queue
from Callback import Callback
from JsonUtils import CRDTEncoder
import json
import socket
from .ServerProvider import ServerProvider

class ServerBase(ServerProvider, ABC):
  def __init__(self, host, port):
    self.host = host
    self.port = port

    self.listeners_running = False
    self.senders_running = False

    self.in_queue = Queue()
    self.out_queue = Queue()

    self.on_recieve = Callback()

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  def send(self, value: object):
    self.out_queue.put(json.dumps(value, cls=CRDTEncoder))
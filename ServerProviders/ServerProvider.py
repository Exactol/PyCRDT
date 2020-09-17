from abc import ABC, abstractmethod
from Callback import Callback

class ServerProvider(ABC):
  on_recieve = Callback()

  @abstractmethod
  def start(self):
    """
    Starts the server
    """
    pass

  @abstractmethod
  def stop(self):
    """
    Stops the server
    """
    pass

  @abstractmethod
  def send(self, value: object):
    """
    Sends data from the server
    """
    pass

  @abstractmethod
  def initialize(self):
    """
    Initializes server, this can be used to perform initial handshakes with remote servers
    """
    pass
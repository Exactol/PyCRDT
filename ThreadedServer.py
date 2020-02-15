import json
import select
import socket
import threading
from queue import Empty, Queue
from typing import List

from Callback import Callback
from JSON.OpSerializer import OpSerializer
from JSON.Payload import Payload


class ThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.listeners_running = False
        self.senders_running = False

        self.in_queue = Queue()
        self.out_queue = Queue()

        self.on_recieve = Callback()

        # initial socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(60)
        # TODO: increase number of listeners?
        self.sock.listen(5)

        self.clients: List[socket.socket] = [self.sock]

    def start(self):
        self.listeners_running = True
        threading.Thread(target=self._listen).start()

    def stop(self):
        print("Shutting down...")
        self.listeners_running = False
        self.senders_running = False

    def _send(self):
        while self.senders_running:
            try:
                data = self.out_queue.get(block=True, timeout=1).encode()
                # send data to each client connected
                for client in self.clients:
                    # send to external clients
                    if client is not self.sock:
                        client.send(data)
            # ignore empty queue errors
            except Empty:
                pass
            except Exception as e:
                print("Send Error:", e)

    def _listen(self):
        # TODO: does this need to increase?
        size = 2048
        # while self.listeners_running:
        #     try:
        #         # wait for new connections with a timeout of 1 second
        #         readable, writable, errored = select.select(self.clients, [], [], 1)
        #         for s in readable: #type: socket.socket
        #             # if s is original socket, new connection is available
        #             if s is self.sock:
        #                 client, address = self.sock.accept()
        #                 print(f"Recieved connection from {address[0]}:{address[1]}")

        #                 # store client
        #                 self.clients.append(client)

        #                 # if sending thread hasnt started yet, start it. will always have atleast 1 client, since server socket is stored in same array
        #                 if (not self.senders_running and len( self.clients ) > 1):
        #                     print("Starting sender thread")
        #                     self.senders_running = True
        #                     threading.Thread(target=self._send).start()

        #                 # TODO: update with current state

        #                 # client.settimeout(60)
        #             # otherwise new data is available from clients
        #             else:
        #                 data = s.recv(size).decode()
        #                 # client disconnected
        #                 if not data or data == "EXIT":
        #                     sock = s.getsockname()
        #                     print(f"{sock[0]}:{sock[1]} disconnected")
        #                     self.clients.remove(s)

        #                     # if all clients disconnect, stop sender thread
        #                     if (self.senders_running and len( self.clients ) == 1):
        #                         print("Stopping sender thread")
        #                         self.senders_running = False
        #                 else:
        #                     data = json.loads(data)
        #                     payload = Payload.from_dict(data)
        #                     self.on_recieve(payload)

        #         for e in errored:
        #             print("ERROR:", e)
        #     except Exception as e:
        #         print(e)

    # TODO: if no clients connected, out_queue will just keep piling up. maybe dont enqueue values if no clients connected
    def send(self, value):
        # serialize with proto buffer
        self.out_queue.put(value.to_proto())

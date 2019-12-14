import select
import socket
import threading
from queue import Empty, Queue
from typing import List


class ThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        self.in_queue = Queue()
        self.out_queue = Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(60)

        self.clients: List[socket.socket] = []

    def start(self):
        threading.Thread(target=self._accept_connections).start()
        threading.Thread(target=self._listen).start()

    def _accept_connections(self):
        self.sock.listen(5)
        print("Listening for connections")
        while self.running:
            # wait for new connections with a timeout of 1 second
            readable, writable, errored = select.select([ self.sock ], [], [], timeout=1)
            print(readable)
            for s in readable:
                if s is self.sock:
                    client, address = self.sock.accept()
                    print(f"Recieved connection from {client}:{address}")

                    # store client
                    self.clients.append(client)

                    client.settimeout(60)



    def stop(self):
        self.running = False
        self.send("EXIT")

    def _send(self):
        while self.running:
            try:
                data = self.out_queue.get(block=True, timeout=1).encode()
                # send data to each client connected
                for client in self.clients:
                    client.send(data)
            except Empty:
                # ignore empty queue errors
                pass
            except Exception as e:
                print(e)

    def _listen(self):
        size = 1024
        while self.running:
            try:
                data = client.recv(size).decode()
                print(data)
                if not data or data == "EXIT":
                    raise "Socket ended"
            except:
                print("Closing socket")
                client.close()
                self.running = False
                return

    def send(self, value):
        self.out_queue.put(value)

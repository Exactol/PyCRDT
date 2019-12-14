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
        # TODO: increase number of listeners?
        self.sock.listen(5)

        self.clients: List[socket.socket] = [self.sock]

    def start(self):
        threading.Thread(target=self._listen).start()

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
                # wait for new connections with a timeout of 1 second
                readable, writable, errored = select.select(self.clients, [], [], 1)
                for s in readable: #type: socket.socket
                    # if s is original socket, new connection is available
                    if s is self.sock:
                        client, address = self.sock.accept()
                        print(f"Recieved connection from {address[0]}:{address[1]}")

                        # store client
                        self.clients.append(client)

                        # TODO: update with current state

                        # client.settimeout(60)
                    # otherwise new data is available from clients
                    else:
                        data = s.recv(size).decode()
                        # client disconnected
                        if not data or data == "EXIT":
                            sock = s.getsockname()
                            print(f"{sock[0]}:{sock[1]} disconnected")
                            self.clients.remove(s)

                        print(data)

                for e in errored:
                    print("ERROR:", e)
            except Exception as e:
                print(e)

    def send(self, value):
        self.out_queue.put(value)

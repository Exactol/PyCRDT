import socket
import threading
from queue import Queue


class ThreadedClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        self.in_queue = Queue()
        self.out_queue = Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((host, port))

    def start(self):
        threading.Thread(target=self._listen).start()
        threading.Thread(target=self._send).start()

    def stop(self):
        self.running = False
        self.send("EXIT")

    def _send(self):
        while self.running:
            data = self.out_queue.get(block=True)
            self.sock.send(data.encode())

    def _listen(self):
        size = 1024
        self.sock.settimeout(60)
        while self.running:
            try:
                data = self.sock.recv(size).decode()
                print(data)
                if not data or data == "EXIT":
                    raise "Socket ended"
            except Exception as e:
                print(e)
                print("Closing socket")
                self.sock.close()
                self.running = False
                return

    def send(self, value):
        self.out_queue.put(value)

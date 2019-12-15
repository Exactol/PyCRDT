import json
import select
import socket
import threading
from queue import Empty, Queue


class ThreadedClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.listeners_running = False
        self.senders_running = False

        self.in_queue = Queue()
        self.out_queue = Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((host, port))
        self.sock.settimeout(60)

    def start(self):
        self.listeners_running = True
        self.senders_running = True

        threading.Thread(target=self._listen).start()
        threading.Thread(target=self._send).start()

    def stop(self):
        print("Shutting down...")
        self.listeners_running = False
        self.senders_running = False

    def _send(self):
        while self.senders_running:
            try:
                data = self.out_queue.get(block=True, timeout=1).encode()
                self.sock.send(data)
            # ignore empty queue errors
            except Empty:
                pass
            except Exception as e:
                print("Send Error:", e)

    def _listen(self):
        # TODO: does this need to increase?
        size = 2048
        while self.listeners_running:
            try:
                readable, writable, errored = select.select([ self.sock ], [], [], 1)
                for s in readable:
                    data = s.recv(size).decode()
                    if not data or data == "EXIT":
                        raise Exception("Socket disconnected")
                    else:
                        data = json.loads(data)
                        print(data)

                for e in errored:
                    print("ERROR:", e)
            except Exception as e:
                print(e)
                print("Closing socket")
                self.sock.close()
                self.running = False
                return

    def send(self, value):
        self.out_queue.put(json.dumps(value))

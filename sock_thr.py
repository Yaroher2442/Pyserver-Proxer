import threading
import queue
from socket import *
import time

"http://192.168.3.121:48080/"

class SockThread(threading.Thread):
    def __init__(self, sock_queue):
        super(SockThread, self).__init__()
        self.sock_queue = sock_queue
        self.conn, self.addr = self.sock_queue.get()
        print("socket thread up")

    def run(self):
        data = self.conn.recv(1024)
        if not data:
            self.conn.close()
            return -1
        else:
            inner_socket = socket(AF_INET, SOCK_STREAM)
            if "server" in str(data):
                inner_socket.connect(("192.168.1.91", 5000))
            else:
                inner_socket.connect(("127.0.0.1", 5000))
            inner_socket.send(data)
            time.sleep(0.001)
            print(data)
            response_data = inner_socket.recv(4000)
            print(response_data)
            self.conn.send(response_data)
            self.conn.close()
            inner_socket.close()
            print("socket thread close")
            return 0

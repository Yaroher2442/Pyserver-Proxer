import threading
import queue
from socket import *
import time
from pprint import pprint

import websockets.headers

from serv_2 import hello
import websockets
import asyncio
import websocket

"/server -> clear /server "
"no /server  redirect -> "
"http://192.168.3.121:48080/"
"ws://192.168.3.121:48088/websocket"


class SockThread(threading.Thread):
    def __init__(self, sock_queue, loop):
        super(SockThread, self).__init__()
        self.sock_queue = sock_queue
        self.conn, self.addr = self.sock_queue.get()
        self.loop = loop
        self.ws = create_connection(address=('192.168.3.121', 48088))
        print("socket thread up")

    def run(self):
        data = self.conn.recv(1024)
        if not data:
            self.conn.close()
            return -1
        else:
            if "Connection: Upgrade" in data.decode('utf-8'):
                buff=data.decode('utf-8')
                data=str(buff[:4]+'/websocket'+buff[5:]).encode()
                self.ws.send(data)
                time.sleep(0.1)
                response = self.ws.recv(1024)
                self.conn.send(response)
                while True:
                    try:
                        request = self.conn.recv(1024)
                        if not request:
                            break
                        print('------------------------------socket------------------------------')
                        self.ws.send(request)
                        time.sleep(0.1)
                        response = self.ws.recv(1024)
                        self.conn.send(response)
                        pprint({'request': data, 'response': response})
                        print('-----------------------------socket-end-----------------------------')
                    except Exception as e:
                        pprint(e)
                        break
                print("socket thread close")
            else:
                print('------------------------------HTTP------------------------------')
                inner_socket = socket(AF_INET, SOCK_STREAM)
                if "server" in data.decode('utf-8'):
                    inner_socket.connect(("192.168.3.121", 48080))
                    buff_ = data.decode('utf-8').replace('/server', '')
                    data = str.encode(buff_)
                else:
                    inner_socket.connect(("127.0.0.1", 5000))
                inner_socket.send(data)
                time.sleep(0.1)
                response_data = inner_socket.recv(4000)
                pprint({'request': data, 'response': response_data})
                self.conn.send(response_data)
                self.conn.close()
                inner_socket.close()
                print('------------------------------HTTP------------------------------')
                print("socket thread close")
        return 0

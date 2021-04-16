import threading
import queue
from socket import *
import time
from pprint import pprint
from ws_serv import WsThreads
from serv_2 import hello
import websockets
import asyncio

"/server -> clear /server "
"no /server  redirect -> "
"http://192.168.3.121:48080/"
"ws://192.168.3.121:48088/websocket"


class SockThread(threading.Thread):
    def __init__(self, sock_queue, loop):
        super(SockThread, self).__init__()
        self.sock_queue = sock_queue
        self.conn, self.addr = self.sock_queue.get()
        self.loop=loop
        print("socket thread up")

    def run(self):
        data = self.conn.recv(1024)
        if not data:
            self.conn.close()
            return -1
        else:
            if "Connection: Upgrade" in str(data):
                # worker = WsThreads(self.conn,self.addr)
                # worker.setDaemon(True)
                # worker.start()
                # worker.join()
                start_server = websockets.serve(hello, self.addr[0], self.addr[1])
                self.loop.run_until_complete(start_server)
                self.loop.run_forever()

            else:
                inner_socket = socket(AF_INET, SOCK_STREAM)
                if "server" in str(data):
                    inner_socket.connect(("192.168.3.121", 48080))
                    buff_ = data.decode('utf-8').replace('/server', '')
                    data = str.encode(buff_)
                else:
                    inner_socket.connect(("127.0.0.1", 5000))
                inner_socket.send(data)
                time.sleep(0.5)
                # print(data)
                response_data = inner_socket.recv(4000)
                # print(response_data)
                pprint({'request': data, 'response': response_data})
                self.conn.send(response_data)
                self.conn.close()
                inner_socket.close()
                print("socket thread close")
        return 0

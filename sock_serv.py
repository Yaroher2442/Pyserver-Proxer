from socket import *
import queue
from sock_thr import SockThread
import asyncio

# данные сервера
host = '0.0.0.0'
port = 9091
addr = (host, port)

sock_queue = queue.Queue()

input_socket = socket(AF_INET, SOCK_STREAM)
input_socket.bind(addr)
input_socket.listen(10)

while True:
    try:
        print('wait connection...')
        conn, addr = input_socket.accept()
        loop=asyncio.get_event_loop()
        print('client addr: ', addr)
        sock_queue.put((conn, addr))
        sock_worker = SockThread(sock_queue, loop)
        sock_worker.setDaemon(True)
        sock_worker.start()
    except KeyboardInterrupt:
        break
print("server closed")
input_socket.close()

from socket import *
import queue
from sock_thr import SockThread

# данные сервера
host = '127.0.0.1'
port = 9090
addr = (host, port)

sock_queue = queue.Queue()

input_socket = socket(AF_INET, SOCK_STREAM)
input_socket.bind(addr)
input_socket.listen(10)

while True:
    try:
        print('wait connection...')
        conn, addr = input_socket.accept()
        print('client addr: ', addr)
        sock_queue.put((conn, addr))
        sock_worker = SockThread(sock_queue)
        sock_worker.setDaemon(True)
        sock_worker.start()
    except KeyboardInterrupt:
        break
print("server closed")
input_socket.close()

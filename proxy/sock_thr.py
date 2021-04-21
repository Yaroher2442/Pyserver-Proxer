import threading
import queue
from socket import *
import time
from pprint import pprint
from loguru import logger
from copy import deepcopy


class SockThread(threading.Thread):

    def __init__(self, sock_queue, configr):
        super(SockThread, self).__init__()
        self.configr = configr
        self.sock_queue = sock_queue
        self.conn, self.addr = self.sock_queue.get()
        self.add_conf()

    def add_conf(self):
        new_level = logger.level("THREAD", no=55, color="<yellow>")
        self.T_logger = logger
        self.T_logger.add('../logs/proxy_threads.log', format="{time:YYYY-MM-DD in HH:mm:ss} {level} {message}",
                          level="THREAD", rotation=self.configr.get_conf("rotation"),
                          compression=self.configr.get_conf("compression"))
        self.T_logger.log("THREAD", f"Socket Thread UP in {self._name}")

    @logger.catch
    def run(self):
        data = self.conn.recv(1024)
        if not data:
            self.conn.close()
            return -1
        else:
            if "Connection: Upgrade" in data.decode('utf-8'):
                try:
                    ws = create_connection(address=(self.configr.get_conf('ws_ip'), self.configr.get_conf('ws_port')))
                    buff = data.decode('utf-8')
                    data = str(buff[:4] + '/websocket' + buff[5:]).encode()
                    ws.send(data)
                    time.sleep(0.1)
                    response = ws.recv(1024)
                    self.conn.send(response)
                    while True:
                        try:
                            request = self.conn.recv(1024)
                            if not request:
                                self.T_logger.log("THREAD", f"Request is empty, connection {self.addr} break ")
                                break
                            ws.send(request)
                            time.sleep(0.1)
                            response = ws.recv(1024)
                            self.conn.send(response)
                            mess_payload = {'request': data, 'response': response}
                            self.T_logger.log("THREAD", f"Message websocket proccesed in {self._name} {mess_payload}")
                            self.T_logger.log("THREAD", f"Socket on thread {str(self)} is closed successfuly")
                            return 0
                        except Exception as e:
                            raise e
                except Exception as e:
                    self.T_logger.error(e)
                    return 0
            else:
                try:
                    inner_socket = socket(AF_INET, SOCK_STREAM)
                    if "server" in data.decode('utf-8'):
                        inner_socket.connect((self.configr.get_conf('b_ip'), self.configr.get_conf('b_port')))
                        buff_ = data.decode('utf-8').replace('/server', '')
                        data = str.encode(buff_)
                    else:
                        inner_socket.connect((self.configr.get_conf('fl_ip'), self.configr.get_conf('fl_port')))
                    inner_socket.send(data)
                    time.sleep(0.1)
                    response = inner_socket.recv(4000)
                    self.conn.send(response)
                    self.conn.close()
                    inner_socket.close()
                    mess_payload = {'request': data, 'response': response}
                    self.T_logger.log("THREAD", f"Message HTTP proccesed in {self._name} {mess_payload}")
                    self.T_logger.log("THREAD", f"Socket on thread {str(self)} is closed successfuly")
                    return 0
                except Exception as e:
                    self.T_logger.error(e)
                    return 0
        return 0

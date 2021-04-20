# Buid-in modules
from socket import *
import queue
import configparser
import os
# pip install modules
from loguru import logger
# Our modules
from sock_thr import SockThread
from config.configorator import Configurator


class Proxy:
    def __init__(self):
        self.configr = Configurator()
        self.input_socket = socket(AF_INET, SOCK_STREAM)
        self.input_socket.bind(host_addr)
        self.input_socket.listen(10)
        self.threads_queue = queue.Queue()

    @logger.catch
    def proxy_loop(self):
        logger.success("Proxy server in up")
        while True:
            try:
                M_logger.success("Server wait for connection")
                conn, addr = self.input_socket.accept()
                M_logger.success(f"Connection from {addr[0]}:{addr[1]} accepted")
                self.threads_queue.put((conn, addr))
                M_logger.success(f"Connection {addr[0]}:{addr[1]} puted in socket queue ")
                sock_worker = SockThread(self.threads_queue)
                sock_worker.setDaemon(True)
                sock_worker.start()
            except Exception as exeption:
                logger.critical(exeption)
                break


if __name__ == '__main__':
    # данные сервера
    configr = Configurator()
    host = configr.get_conf("MAIN_LOOP", "host_ip")
    port = configr.get_conf("MAIN_LOOP", "host_port")
    host_addr = (host, port)

    rotation_logs = configr.get_conf("LOGGER", "rotation")
    compression_logs = configr.get_conf("LOGGER", "compression")
    M_logger = logger
    M_logger.add('../logs/proxy_all.log', format="{time:YYYY-MM-DD in HH:mm:ss} | {level} | {message}",
                 level="DEBUG", rotation=rotation_logs, compression=compression_logs)

    proxy = Proxy()
    proxy.proxy_loop()

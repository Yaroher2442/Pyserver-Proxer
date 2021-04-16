import threading
import asyncio
import websockets


class WsThreads(threading.Thread):
    def __init__(self, conn, addr):
        super(WsThreads, self).__init__()
        self.REMOTE_URL = "ws://192.168.3.121:48088/websocket"
        self.conn = conn
        self.addr = addr

    def hello(self, websocket, path):
        '''Called whenever a new connection is made to the server'''
        url = self.REMOTE_URL + path
        print(url)
        with websockets.connect(url) as ws:
            self.clientToServer(ws, websocket)
            self.serverToClient(ws, websocket)

    def clientToServer(self, ws, websocket):
        for message in ws:
            websocket.send(message)

    def serverToClient(self, ws, websocket):
        for message in websocket:
            ws.send(message)

    def run(self):
        host = "localhost"
        port = 8765
        start_server = websockets.serve(self.hello, self.addr[0], self.addr[1])

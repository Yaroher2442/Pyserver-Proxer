import argparse
import asyncio
import websockets

REMOTE_URL = "ws://192.168.3.121:48088/websocket"


async def hello(websocket, path):
    '''Called whenever a new connection is made to the server'''

    url = REMOTE_URL + path
    print(url)
    async with websockets.connect(url) as ws:
        taskA = asyncio.create_task(clientToServer(ws, websocket))
        taskB = asyncio.create_task(serverToClient(ws, websocket))

        await taskA
        await taskB


async def clientToServer(ws, websocket):
    async for message in ws:
        await websocket.send(message)


async def serverToClient(ws, websocket):
    async for message in websocket:
        await ws.send(message)


if __name__ == '__main__':
    host = "localhost"
    port = 8765

    start_server = websockets.serve(hello, host, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

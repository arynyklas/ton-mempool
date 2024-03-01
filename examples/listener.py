import asyncio
import json
import os

import websockets


async def processor(query: bytes):
    print('got', query)


async def listener():
    PORT = os.getenv("PORT", 8765)
    uri = f"ws://localhost:{PORT}"
    while True:
        async with websockets.connect(uri) as websocket:
            try:
                # can send external
                boc = 'b5ee9c720101020100bc0001e188011e132a6fdfcd0544c797034802e1d23d7cfc63c8c48e93ecd82dbd3c2fa1d23a034893878c5c525b638ef99c89f4751ff73e7b28bd80495195cfb0cf53a85d1dd88fea1d7e11a54d918fb3c7e29358844b910d9874beaaf5a17f223ceed2ece0494d4d18bb2f0e4df000000240001c01008c42004784ca9bf7f3415131e5c0d200b8748f5f3f18f23123a4fb360b6f4f0be8748ea017d78400000000000000000000000000000000000074657374206f7665726c61792034'
                await websocket.send(json.dumps({'type': 'send_external', 'data': boc}).encode())
                await websocket.send(json.dumps({'type': 'get_peers_amount'}).encode())
                while True:
                    ext = await websocket.recv()
                    await processor(ext)  # pass your processor here
            except websockets.ConnectionClosed:
                continue


if __name__ == "__main__":
    asyncio.run(listener())
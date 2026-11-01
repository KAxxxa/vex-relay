# language: python, file: server.py
import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Просто пересылаем всё всем остальным
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000, max_size=10*1024*1024):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            for client in clients:
                if client != websocket:
                    await client.send(json.dumps(data))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

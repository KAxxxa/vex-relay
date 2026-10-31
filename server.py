# language: python, file: server.py
import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    try:
                        await client.send(message)
                    except:
                        pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("Server started on port 10000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
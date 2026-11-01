import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Отправляем всем, кроме отправителя
            for client in clients:
                if client != websocket:
                    await client.send(message)
            
            # Если кто-то зашел/вышел, обновляем счетчик онлайна
            if data.get("type") in ("join", "leave"):
                count = len(clients)
                for client in clients:
                    await client.send(json.dumps({"type": "online", "count": count}))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)
        # Обновляем счетчик при выходе
        count = len(clients)
        for client in clients:
            try:
                await client.send(json.dumps({"type": "online", "count": count}))
            except: pass

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000, max_size=10*1024*1024):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

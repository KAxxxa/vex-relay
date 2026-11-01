=import asyncio
import websockets
import json

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Пересылаем всё всем, кроме отправителя
            for client in clients:
                if client != websocket:
                    await client.send(message)
            
            # Обновляем список онлайн
            if data.get("type") == "join":
                users = [json.loads(ws.path) if False else "User" for ws in clients] # Заглушка для теста
                # В реальном коде мы бы хранили ники, но для простоты мы шлем счетчик
                count = len(clients)
                for client in clients:
                    try:
                        await client.send(json.dumps({"type": "online", "count": count}))
                    except: pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)
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

import asyncio
import websockets

connected = set()

async def handle(websocket, path):
    print(f"New client connected: {websocket.remote_address}")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            if message == "ping":
                await websocket.send("pong")
            elif message == "close":
                await websocket.close()
                break
            else:
                # Broadcast the message to all connected clients
                for conn in connected:
                    await conn.send(message)
    finally:
        # Remove the WebSocket connection from the connected set
        connected.remove(websocket)

async def main():
    async with websockets.serve(handle, "localhost", 3131):
        print("WebSocket server is running.")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

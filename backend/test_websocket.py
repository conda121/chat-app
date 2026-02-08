import asyncio
import websockets
import json
import sys

async def test_websocket(token: str, channel_id: int, username: str):
    uri = f"ws://localhost:8000/ws/{channel_id}?token={token}"
    
    print(f"[{username}] Connecting to channel {channel_id}...")
    
    async with websockets.connect(uri) as websocket:
        print(f"[{username}] Connected!")
        
        # Start listening for messages
        async def receive_messages():
            try:
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print(f"\n[{username}] Received: {data['type']}")
                    print(f"  From: {data['username']}")
                    print(f"  Message: {data['content']}")
                    print(f"  Time: {data['timestamp']}")
            except websockets.exceptions.ConnectionClosed:
                print(f"[{username}] Connection closed")
        
        # Start sending messages
        async def send_messages():
            await asyncio.sleep(2)  # Wait for connection to stabilize
            
            messages = [
                "Hello everyone!",
                "How are you doing?",
                "WebSocket is working great!"
            ]
            
            for msg in messages:
                await asyncio.sleep(3)  # Wait 3 seconds between messages
                message_data = {
                    "content": msg
                }
                await websocket.send(json.dumps(message_data))
                print(f"[{username}] Sent: {msg}")
        
        # Run both tasks concurrently
        await asyncio.gather(
            receive_messages(),
            send_messages()
        )

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python test_websocket.py <token> <channel_id> <username>")
        sys.exit(1)
    
    token = sys.argv[1]
    channel_id = int(sys.argv[2])
    username = sys.argv[3]
    
    asyncio.run(test_websocket(token, channel_id, username))

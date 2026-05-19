import asyncio
import websockets


async def test():

    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:

        print("Connected")

        # Receive first bot message
        bot_message = await websocket.recv()

        print("BOT:", bot_message)

        while True:

            user_input = input("You: ")

            await websocket.send(user_input)

            bot_message = await websocket.recv()

            print("BOT:", bot_message)


asyncio.run(test())
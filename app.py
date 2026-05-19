from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket

from websocket.voice_socket import (
    handle_voice
)

from database.db import init_db


# Initialize SQLite DB
init_db()

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await handle_voice(
        websocket
    )
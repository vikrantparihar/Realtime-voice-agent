# Realtime AI Voice Agent

## Install

```bash
pip install -r requirements.txt
```

## Add API Keys

Rename:

.env.example → .env

Add:
- OpenAI API Key
- Deepgram API Key
- ElevenLabs API Key

## Run

```bash
uvicorn app:app --reload
```

## Open

http://127.0.0.1:8000

## WebSocket Endpoint

ws://127.0.0.1:8000/ws/voice

## Features

- Deterministic FSM
- Multi-slot extraction
- Over-answer handling
- Deepgram STT
- ElevenLabs TTS
- OpenAI extraction
- Realtime websocket architecture

# Realtime AI Voice Agent

Realtime stateful AI voice agent with streaming STT/TTS, deterministic orchestration, slot extraction, conversational memory, and websocket infrastructure.

---

# Features

- Realtime bidirectional voice streaming
- Deterministic FSM-based orchestration
- Multi-slot entity extraction
- Over-answer handling
- Streaming Speech-to-Text
- Streaming Text-to-Speech
- Conversational memory
- Vector memory support
- WebSocket-based realtime communication
- Modular architecture for production scalability

---

# Architecture

```text
Client Audio
    ↓
WebSocket Server
    ↓
Streaming STT (Deepgram)
    ↓
Orchestrator / FSM
    ↓
LLM Extraction + Reasoning
    ↓
Memory + Vector Memory
    ↓
Streaming TTS (ElevenLabs)
    ↓
Client Audio Response
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Realtime Transport | WebSockets |
| STT | Deepgram |
| TTS | ElevenLabs |
| LLM | OpenAI |
| Memory | Custom Stateful Memory |
| Vector Store | Vector Memory Layer |
| Architecture | Deterministic FSM |

---

# Repository Structure

```text
Realtime-voice-agent/
│
├── app.py
├── requirements.txt
├── .env.example
│
├── orchestrator/      # Deterministic conversation flow
├── llm/               # LLM extraction and reasoning
├── stt/               # Speech-to-text pipeline
├── tts/               # Text-to-speech pipeline
├── websocket/         # Realtime websocket handlers
├── memory/            # Stateful conversational memory
├── vector_memory/     # Semantic retrieval layer
├── database/          # Persistence layer
├── frontend/          # Client frontend
├── logs/              # Runtime logs
│
└── test_client.py
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/vikrantparihar/Realtime-voice-agent.git

cd Realtime-voice-agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Rename:

```text
.env.example → .env
```

Add the following keys:

```env
OPENAI_API_KEY=
DEEPGRAM_API_KEY=
ELEVENLABS_API_KEY=
```

---

# Running the Application

```bash
uvicorn app:app --reload
```

Server starts at:

```text
http://127.0.0.1:8000
```

---

# WebSocket Endpoint

```text
ws://127.0.0.1:8000/ws/voice
```

---

# Conversation Orchestration

The system uses a deterministic finite-state-machine (FSM) architecture instead of relying entirely on prompting.

Benefits:

- Better controllability
- Reduced hallucinations
- Structured slot extraction
- Reliable conversational transitions
- Production-friendly conversational flows

---

# Memory System

The project contains two memory layers:

## Stateful Memory

Stores:
- user session state
- extracted slots
- dialogue progress

## Vector Memory

Stores:
- semantic conversation embeddings
- contextual retrieval data
- long-term conversational context

---

# Realtime Pipeline

## Input Flow

```text
Microphone Audio
→ WebSocket Stream
→ Deepgram Streaming STT
→ Transcript Processing
```

## Output Flow

```text
LLM Response
→ ElevenLabs Streaming TTS
→ Audio Chunks
→ Client Playback
```

---

# Current Capabilities

- Realtime voice conversations
- Structured information extraction
- Multi-turn stateful dialogue
- Interrupt-safe orchestration
- Modular AI pipeline design

---

# Future Improvements

- Voice activity detection (VAD)
- Barge-in interruption handling
- Redis session store
- Docker deployment
- Kubernetes scaling
- Telephony integration
- Twilio support
- Streaming token generation
- Observability dashboards

---

# Example Use Cases

- AI Call Assistants
- Voice-based Customer Support
- Healthcare Intake Systems
- Conversational AI Agents
- Realtime AI Receptionists
- AI Interview Systems

---

# Development

## Run Test Client

```bash
python test_client.py
```

---

# Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you would like to change.

---

# License

MIT License

---

# Author

Vikrant Singh Parihar

GitHub:
https://github.com/vikrantparihar

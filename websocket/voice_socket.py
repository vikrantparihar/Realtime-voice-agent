# websocket/voice_socket.py

import uuid
import time
import asyncio

from memory.redis_session_store import (
    get_session,
    save_session,
    update_slot,
    add_event,
    increment_retries,
    reset_retries,
    all_slots_verified
)

from stt.deepgram_client import DeepgramStreamingClient

# ✅ SIMPLE REGEX EXTRACTOR
from llm.extractor import extract_entities

from logs.logger import log_message

from orchestrator.validator import (
    validate_name,
    validate_pan,
    validate_dob
)

from orchestrator.question_engine import get_next_question
from orchestrator.flow_engine import FlowEngine

from orchestrator.states import (
    CALL_STARTED,
    ASKING_QUESTION,
    LISTENING,
    PROCESSING,
    VERIFYING,
    COMPLETED,
    FAILED
)

from orchestrator.escalation import escalate_to_human
from tts.tts_worker import stream_tts_audio


# ---------------------------------
# MAIN ENTRY
# ---------------------------------

async def handle_voice(websocket):

    await websocket.accept()

    session_id = str(uuid.uuid4())

    session = get_session(session_id)

    # ---------------------------------
    # NEW SESSION
    # ---------------------------------

    if not session:

        session = {

            "session_id": session_id,

            "state": CALL_STARTED,

            "current_question_index": 0,

            "last_activity": time.time(),

            "is_bot_speaking": False,

            "user_interrupt": False,

            "history": [],

            "retries": 0,

            "slots": {

                "full_name": {"value": None},

                "dob": {"value": None},

                "pan": {"value": None},

                "address": {"value": None},

                "email": {"value": None},

                "mobile": {"value": None},

                "father_name": {"value": None},

                "occupation": {"value": None},

                "city": {"value": None},

                "income": {"value": None}
            }
        }

    save_session(session_id, session)

    # ---------------------------------
    # FLOW ENGINE
    # ---------------------------------

    flow = FlowEngine(session)

    # ---------------------------------
    # DEEPGRAM INIT
    # ---------------------------------

    deepgram = DeepgramStreamingClient()

    await deepgram.connect()

    # ---------------------------------
    # ASK FIRST QUESTION
    # ---------------------------------

    session["state"] = ASKING_QUESTION

    save_session(session_id, session)

    first_q = get_next_question(session)

    print("BOT:", first_q)

    await websocket.send_text(first_q)

    session["state"] = LISTENING

    save_session(session_id, session)

    # ---------------------------------
    # MAIN LOOP
    # ---------------------------------

    try:

        while True:

            # ---------------------------------
            # RECEIVE AUDIO
            # ---------------------------------

            audio_chunk = await websocket.receive_bytes()

            if not audio_chunk:
                continue

            session["last_activity"] = time.time()

            save_session(session_id, session)

            # ---------------------------------
            # SEND AUDIO TO DEEPGRAM
            # ---------------------------------

            await deepgram.send_audio(audio_chunk)

            # ---------------------------------
            # WAIT FOR TRANSCRIPT
            # ---------------------------------

            if deepgram.transcript_queue.empty():
                continue

            stt_result = await deepgram.get_transcript()

            if not stt_result.get("is_final"):
                continue

            transcript = stt_result.get(
                "text",
                ""
            ).strip()

            confidence = stt_result.get(
                "confidence",
                0
            )

            # ---------------------------------
            # LOW CONFIDENCE FILTER
            # ---------------------------------

            if confidence < 0.70:

                print(
                    "LOW CONFIDENCE SKIPPED"
                )

                continue

            # ---------------------------------
            # EMPTY TRANSCRIPT
            # ---------------------------------

            if not transcript:
                continue

            print(
                "USER:",
                transcript
            )

            print(
                "CONF:",
                confidence
            )

            log_message(
                "USER",
                transcript
            )

            # ---------------------------------
            # ENTITY EXTRACTION
            # ---------------------------------

            entities = extract_entities(
                transcript
            )

            print(
                "EXTRACTED:",
                entities
            )

            # ---------------------------------
            # FLOW ENGINE
            # ---------------------------------

            filled = flow.process(
                entities
            )

            # ---------------------------------
            # UPDATE SLOTS
            # ---------------------------------

            for k, v in filled.items():

                update_slot(
                    session,
                    k,
                    v
                )

                add_event(
                    session,
                    "SLOT_CAPTURED",
                    {k: v}
                )

                print(
                    "SLOT UPDATED:",
                    k,
                    "=",
                    v
                )

            save_session(
                session_id,
                session
            )

            # ---------------------------------
            # COMPLETION CHECK
            # ---------------------------------

            if all_slots_verified(session):

                session["state"] = COMPLETED

                save_session(
                    session_id,
                    session
                )

                completion_msg = (
                    "Verification completed successfully"
                )

                print(
                    "BOT:",
                    completion_msg
                )

                await websocket.send_text(
                    completion_msg
                )

                break

            # ---------------------------------
            # NEXT QUESTION
            # ---------------------------------

            next_q = get_next_question(
                session
            )

            print(
                "BOT:",
                next_q
            )

            await websocket.send_text(
                next_q
            )

    # ---------------------------------
    # ERROR HANDLING
    # ---------------------------------

    except Exception as e:

        session["state"] = FAILED

        save_session(
            session_id,
            session
        )

        print(
            "WEBSOCKET ERROR:",
            str(e)
        )

    # ---------------------------------
    # CLEANUP
    # ---------------------------------

    finally:

        try:

            await websocket.close()

        except:

            pass
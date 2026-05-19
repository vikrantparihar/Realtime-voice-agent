from datetime import datetime

from orchestrator.states import (
    CALL_STARTED
)

# -----------------------------------
# GLOBAL IN-MEMORY SESSION STORE
# -----------------------------------

sessions = {}

# -----------------------------------
# CREATE / GET SESSION
# -----------------------------------

def get_session(session_id):

    if session_id not in sessions:

        sessions[session_id] = {

            # -----------------------------------
            # SESSION INFO
            # -----------------------------------

            "session_id": session_id,

            "created_at": str(
                datetime.utcnow()
            ),

            "last_activity": str(
                datetime.utcnow()
            ),

            # -----------------------------------
            # CALL STATE
            # -----------------------------------

            "state": CALL_STARTED,

            "call_status": "IN_PROGRESS",

            # -----------------------------------
            # HUMAN HANDOFF
            # -----------------------------------

            "agent_required": False,

            "handoff_reason": None,

            # -----------------------------------
            # QUESTION FLOW
            # -----------------------------------

            "question_index": 0,

            "current_question":
            "Please tell your full name.",

            # -----------------------------------
            # BOT SPEAKING STATE
            # -----------------------------------

            "is_bot_speaking": False,

            # -----------------------------------
            # USER INTERRUPT
            # -----------------------------------

            "user_interrupt": False,

            # -----------------------------------
            # STRUCTURED MEMORY
            # -----------------------------------

            "slots": {

                "full_name": {
                    "value": None,
                    "verified": False
                },

                "dob": {
                    "value": None,
                    "verified": False
                },

                "pan": {
                    "value": None,
                    "verified": False
                },

                "address": {
                    "value": None,
                    "verified": False
                },

                "email": {
                    "value": None,
                    "verified": False
                },

                "mobile": {
                    "value": None,
                    "verified": False
                },

                "father_name": {
                    "value": None,
                    "verified": False
                },

                "occupation": {
                    "value": None,
                    "verified": False
                },

                "city": {
                    "value": None,
                    "verified": False
                },

                "income": {
                    "value": None,
                    "verified": False
                }
            },

            # -----------------------------------
            # CONVERSATION HISTORY
            # -----------------------------------

            "history": [],

            # -----------------------------------
            # EVENT LOGS
            # -----------------------------------

            "events": [],

            # -----------------------------------
            # RETRY TRACKING
            # -----------------------------------

            "retry_count": 0,

            "max_retries": 3,

            # -----------------------------------
            # LAST BOT PROMPT
            # -----------------------------------

            "last_bot_prompt": None,

            # -----------------------------------
            # LAST USER TRANSCRIPT
            # -----------------------------------

            "last_transcript": None,

            # -----------------------------------
            # STT CONFIDENCE
            # -----------------------------------

            "confidence": 0.0
        }

    return sessions[session_id]


# -----------------------------------
# UPDATE SLOT
# -----------------------------------

def update_slot(
    session,
    slot_name,
    value
):

    if slot_name not in session["slots"]:

        return

    session["slots"][slot_name]["value"] = value

    session["slots"][slot_name]["verified"] = True


# -----------------------------------
# GET SLOT
# -----------------------------------

def get_slot(
    session,
    slot_name
):

    if slot_name not in session["slots"]:

        return None

    return session["slots"][slot_name]["value"]


# -----------------------------------
# CHECK ALL VERIFIED
# -----------------------------------

def all_slots_verified(session):

    for slot_data in session["slots"].values():

        if not slot_data["value"]:

            return False

    return True


# -----------------------------------
# UPDATE ACTIVITY
# -----------------------------------

def update_activity(session):

    session["last_activity"] = str(
        datetime.utcnow()
    )


# -----------------------------------
# RESET RETRIES
# -----------------------------------

def reset_retries(session):

    session["retry_count"] = 0


# -----------------------------------
# INCREMENT RETRIES
# -----------------------------------

def increment_retries(session):

    session["retry_count"] += 1

    return session["retry_count"]


# -----------------------------------
# ADD EVENT
# -----------------------------------

def add_event(
    session,
    event_type,
    payload
):

    session["events"].append({

        "timestamp": str(
            datetime.utcnow()
        ),

        "type": event_type,

        "payload": payload
    })
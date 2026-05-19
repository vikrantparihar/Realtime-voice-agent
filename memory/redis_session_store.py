import json
import redis
import time


# -----------------------------------
# REDIS CLIENT
# -----------------------------------

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


# -----------------------------------
# INTERNAL UTIL
# -----------------------------------

def _session_key(session_id):

    return f"session:{session_id}"


# -----------------------------------
# CREATE / SAVE SESSION
# -----------------------------------

def save_session(session_id, data):

    # IMPORTANT FIX
    # Always store numeric timestamp
    data["last_activity"] = time.time()

    r.set(
        _session_key(session_id),
        json.dumps(data)
    )


# -----------------------------------
# GET SESSION
# -----------------------------------

def get_session(session_id):

    data = r.get(
        _session_key(session_id)
    )

    if not data:
        return None

    session = json.loads(data)

    # SAFETY FIX
    if "last_activity" not in session:

        session["last_activity"] = time.time()

    return session


# -----------------------------------
# UPDATE SLOT
# -----------------------------------

def update_slot(session, key, value):

    if "slots" not in session:

        session["slots"] = {}

    if key not in session["slots"]:

        session["slots"][key] = {
            "value": None
        }

    session["slots"][key]["value"] = value

    # STORE FILL TIME
    session["slots"][key]["filled_at"] = time.time()


# -----------------------------------
# EVENT LOGGING
# -----------------------------------

def add_event(session, event_type, data):

    if "events" not in session:

        session["events"] = []

    session["events"].append({

        "type": event_type,

        "data": data,

        "time": time.time()
    })


# -----------------------------------
# RETRY HANDLING
# -----------------------------------

def increment_retries(session):

    session["retries"] = (
        session.get("retries", 0) + 1
    )

    return session["retries"]


def reset_retries(session):

    session["retries"] = 0


# -----------------------------------
# ACTIVITY UPDATE
# -----------------------------------

def update_activity(session):

    session["last_activity"] = time.time()


# -----------------------------------
# COMPLETION CHECK
# -----------------------------------

def all_slots_verified(session):

    if "slots" not in session:

        return False

    for slot in session["slots"].values():

        if slot.get("value") is None:

            return False

    return True


# -----------------------------------
# PATCH SESSION
# -----------------------------------

def patch_session(session_id, patch_dict):

    session = get_session(session_id)

    if not session:

        return None

    session.update(patch_dict)

    session["last_activity"] = time.time()

    save_session(
        session_id,
        session
    )

    return session


# -----------------------------------
# EVENT + SAVE
# -----------------------------------

def log_event_and_save(
    session_id,
    session,
    event_type,
    data
):

    add_event(
        session,
        event_type,
        data
    )

    save_session(
        session_id,
        session
    )
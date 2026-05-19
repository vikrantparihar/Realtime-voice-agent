from orchestrator.states import (
    CALL_STARTED,
    ASKING_QUESTION,
    WAITING_FOR_RESPONSE,
    VALIDATING_RESPONSE,
    VERIFICATION_COMPLETE,
    CALL_ESCALATED
)

from memory.session_memory import (
    all_slots_verified
)


# -----------------------------------
# UPDATE STATE
# -----------------------------------

def set_state(
    session,
    new_state
):

    old_state = session["state"]

    session["state"] = new_state

    print(
        f"STATE TRANSITION: "
        f"{old_state} -> {new_state}"
    )


# -----------------------------------
# START CALL
# -----------------------------------

def start_call(session):

    set_state(
        session,
        ASKING_QUESTION
    )


# -----------------------------------
# WAITING USER
# -----------------------------------

def wait_for_user(session):

    set_state(
        session,
        WAITING_FOR_RESPONSE
    )


# -----------------------------------
# VALIDATING
# -----------------------------------

def validating(session):

    set_state(
        session,
        VALIDATING_RESPONSE
    )


# -----------------------------------
# COMPLETE CALL
# -----------------------------------

def complete_call(session):

    set_state(
        session,
        VERIFICATION_COMPLETE
    )

    session[
        "call_status"
    ] = "COMPLETED"


# -----------------------------------
# ESCALATE CALL
# -----------------------------------

def escalate_call(session):

    set_state(
        session,
        CALL_ESCALATED
    )

    session[
        "call_status"
    ] = "ESCALATED"


# -----------------------------------
# CHECK COMPLETION
# -----------------------------------

def check_completion(session):

    if all_slots_verified(
        session
    ):

        complete_call(
            session
        )

        return True

    return False
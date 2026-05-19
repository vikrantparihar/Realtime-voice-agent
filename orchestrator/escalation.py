# orchestrator/escalation.py

from datetime import datetime


# -----------------------------------
# ESCALATE TO HUMAN AGENT
# -----------------------------------

def escalate_to_human(
    session,
    reason="UNKNOWN"
):

    # -----------------------------------
    # UPDATE SESSION
    # -----------------------------------

    session[
        "call_status"
    ] = "ESCALATED"

    session[
        "escalation_reason"
    ] = reason

    session[
        "escalated_at"
    ] = str(
        datetime.utcnow()
    )

    # -----------------------------------
    # LOG
    # -----------------------------------

    print(
        "CALL ESCALATED TO HUMAN:",
        reason
    )

    # -----------------------------------
    # RESPONSE MESSAGE
    # -----------------------------------

    return (
        "Verification failed. "
        "Connecting you to a human agent."
    )
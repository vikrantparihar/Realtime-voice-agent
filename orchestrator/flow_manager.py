from orchestrator.question_engine import (
    get_current_question,
    move_next
)

from llm.extractor import (
    extract_entities
)

from orchestrator.validator import (
    validate_name,
    validate_pan,
    validate_dob
)


def process_user_input(session, user_text):

    print("\n===== NEW USER INPUT =====")
    print("USER TEXT:", user_text)

    VALIDATORS = {
        "full_name": validate_name,
        "dob": validate_dob,
        "pan": validate_pan
    }

    # -------------------------
    # CURRENT QUESTION
    # -------------------------

    current = get_current_question(session)

    if current is None:

        return (
            "Verification completed successfully."
        )

    expected_slot = current["slot"]

    print("EXPECTED SLOT:", expected_slot)

    # -------------------------
    # EXTRACT ENTITIES
    # -------------------------

    entities = extract_entities(user_text)

    # SAFETY CHECKS

    if entities is None:
        entities = {}

    if not isinstance(entities, dict):
        entities = {}

    print("EXTRACTED:", entities)

    # -------------------------
    # ONLY PROCESS EXPECTED SLOT
    # -------------------------

    if expected_slot in entities:

        value = entities[expected_slot]

        validator = VALIDATORS.get(expected_slot)

        # -------------------------
        # VALIDATION SUCCESS
        # -------------------------

        if validator and validator(value):

            session["slots"][expected_slot] = value

            session["retry_count"] = 0

            print(f"{expected_slot} VALID")

        # -------------------------
        # VALIDATION FAILURE
        # -------------------------

        else:

            session["retry_count"] += 1

            print(
                "RETRY COUNT:",
                session["retry_count"]
            )

            if session["retry_count"] >= 3:

                return (
                    "Verification failed. "
                    "Transferring to human agent."
                )

            return (
                f"The provided {expected_slot} "
                "seems invalid. "
                "Please repeat carefully."
            )

    # -------------------------
    # ENTITY NOT DETECTED
    # -------------------------

    else:

        session["retry_count"] += 1

        print(
            "ENTITY NOT DETECTED"
        )

        print(
            "RETRY COUNT:",
            session["retry_count"]
        )

        if session["retry_count"] >= 3:

            return (
                "I am unable to verify the information. "
                "Transferring to human agent."
            )

        return (
            f"I could not detect your "
            f"{expected_slot}. "
            "Please repeat clearly."
        )

    # -------------------------
    # MOVE THROUGH FILLED SLOTS
    # -------------------------

    while True:

        current = get_current_question(session)

        if current is None:

            print(
                "VERIFICATION COMPLETED"
            )

            return (
                "Verification completed successfully."
            )

        slot_name = current["slot"]

        if session["slots"].get(slot_name):

            print(
                f"SLOT '{slot_name}' ALREADY FILLED"
            )

            move_next(session)

        else:

            break

    # -------------------------
    # NEXT QUESTION
    # -------------------------

    print(
        "NEXT QUESTION:",
        current["question"]
    )

    return current["question"]
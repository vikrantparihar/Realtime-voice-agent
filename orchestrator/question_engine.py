QUESTION_FLOW = [

    {
        "slot": "full_name",
        "prompt": "Please tell your full name."
    },

    {
        "slot": "dob",
        "prompt": "Please tell your date of birth."
    },

    {
        "slot": "pan",
        "prompt": "Please tell your PAN number."
    },

    {
        "slot": "address",
        "prompt": "Please tell your address."
    },

    {
        "slot": "email",
        "prompt": "Please tell your email address."
    },

    {
        "slot": "mobile",
        "prompt": "Please tell your mobile number."
    },

    {
        "slot": "father_name",
        "prompt": "Please tell your father's name."
    },

    {
        "slot": "occupation",
        "prompt": "Please tell your occupation."
    },

    {
        "slot": "city",
        "prompt": "Please tell your city."
    },

    {
        "slot": "income",
        "prompt": "Please tell your annual income."
    }

]


# ---------------------------------
# GET NEXT QUESTION
# ---------------------------------

def get_next_question(session):

    slots = session["slots"]

    for question in QUESTION_FLOW:

        slot_name = question["slot"]

        # -------------------------
        # SLOT NOT PRESENT
        # -------------------------

        if slot_name not in slots:

            continue

        # -------------------------
        # SLOT EMPTY
        # -------------------------

        if not slots[
            slot_name
        ][
            "value"
        ]:

            session[
                "current_question"
            ] = question[
                "prompt"
            ]

            return question[
                "prompt"
            ]

    # ---------------------------------
    # ALL QUESTIONS COMPLETED
    # ---------------------------------

    return (
        "Verification completed successfully."
    )
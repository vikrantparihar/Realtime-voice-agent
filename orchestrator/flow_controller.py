SLOTS_ORDER = [
    "full_name",
    "dob",
    "pan",
    "address",
    "email",
    "mobile",
    "father_name",
    "occupation",
    "city",
    "income"
]

def get_current_step(session):
    return session.get("current_step", 0)


def get_current_slot(session):
    step = get_current_step(session)
    if step >= len(SLOTS_ORDER):
        return None
    return SLOTS_ORDER[step]


def move_next(session):
    session["current_step"] = session.get("current_step", 0) + 1
    return session["current_step"]


def is_flow_complete(session):
    return session.get("current_step", 0) >= len(SLOTS_ORDER)
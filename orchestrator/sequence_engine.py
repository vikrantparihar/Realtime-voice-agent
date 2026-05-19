QUESTIONS = [
    "What is your full name?",
    "What is your date of birth?",
    "What is your PAN number?",
    "What is your address?",
    "What is your email?",
    "What is your mobile number?",
    "What is your father's name?",
    "What is your occupation?",
    "Which city do you live in?",
    "What is your monthly income?"
]


def get_current_question(session):
    idx = session.get("current_step", 0)

    if idx >= len(QUESTIONS):
        return None

    return QUESTIONS[idx]


def move_next(session):
    session["current_step"] = session.get("current_step", 0) + 1
    return session


def reset_sequence(session):
    session["current_step"] = 0
    return session
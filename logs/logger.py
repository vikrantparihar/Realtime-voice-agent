from datetime import datetime


def log_message(
    role,
    text
):

    with open(
        "call_logs.txt",
        "a"
    ) as f:

        f.write(
            f"[{datetime.now()}] "
            f"{role}: "
            f"{text}\n"
        )
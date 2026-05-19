import re
from datetime import datetime


def validate_name(name):

    if len(name.strip()) < 2:

        return False

    return True


def validate_pan(pan):

    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'

    return bool(
        re.match(pattern, pan)
    )


def validate_dob(dob):

    try:

        datetime.strptime(
            dob,
            "%d %B %Y"
        )

        return True

    except:

        return False
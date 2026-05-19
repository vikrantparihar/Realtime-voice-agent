import re


def extract_entities(
    text
):

    result = {}

    # ---------------------------------
    # CLEAN INPUT
    # ---------------------------------

    text = (
        text
        .strip()
    )

    # ---------------------------------
    # FULL NAME
    # ---------------------------------

    name_match = re.search(

        r'my name is\s+([a-zA-Z\s]+?)(,|\.|and|dob|pan|address|email|mobile|$)',

        text,

        re.IGNORECASE
    )

    if name_match:

        result[
            "full_name"
        ] = (

            name_match
            .group(1)

            .strip()

            .title()
        )

    # ---------------------------------
    # DOB
    # ---------------------------------

    dob_match = re.search(

        r'(\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',

        text,

        re.IGNORECASE
    )

    if dob_match:

        result[
            "dob"
        ] = (
            dob_match
            .group(1)
        )

    # ---------------------------------
    # PAN
    # ---------------------------------

    pan_match = re.search(

        r'pan (number )?is\s+([A-Z]{5}[0-9]{4}[A-Z])',

        text,ml,

        re.IGNORECASE
    )

    if pan_match:

        result[
            "pan"
        ] = (

            pan_match
            .group(2)

            .strip()

            .upper()
        )

    # ---------------------------------
    # ADDRESS
    # ---------------------------------

    address_match = re.search(

        r'address is\s+(.+?)(,|\.|$)',

        text,

        re.IGNORECASE
    )

    if address_match:

        result[
            "address"
        ] = (

            address_match
            .group(1)

            .strip()

            .title()
        )

    # ---------------------------------
    # EMAIL
    # ---------------------------------

    email_match = re.search(

        r'[\w\.-]+@[\w\.-]+\.\w+',

        text,

        re.IGNORECASE
    )

    if email_match:

        result[
            "email"
        ] = (

            email_match
            .group(0)

            .strip()

            .lower()
        )

    # ---------------------------------
    # MOBILE
    # ---------------------------------

    mobile_match = re.search(

        r'(\+91)?[\s\-]?[6-9]\d{9}',

        text
    )

    if mobile_match:

        result[
            "mobile"
        ] = (

            mobile_match
            .group(0)

            .replace(
                " ",
                ""
            )

            .replace(
                "-",
                ""
            )
        )

    # ---------------------------------
    # FATHER NAME
    # ---------------------------------

    father_match = re.search(

        r'father.?s name is\s+([a-zA-Z\s]+)',

        text,

        re.IGNORECASE
    )

    if father_match:

        result[
            "father_name"
        ] = (

            father_match
            .group(1)

            .strip()

            .title()
        )

    # ---------------------------------
    # OCCUPATION
    # ---------------------------------

    occupation_match = re.search(

        r'i am a[n]?\s+([a-zA-Z\s]+)',

        text,

        re.IGNORECASE
    )

    if occupation_match:

        result[
            "occupation"
        ] = (

            occupation_match
            .group(1)

            .strip()

            .title()
        )

    # ---------------------------------
    # CITY
    # ---------------------------------

    city_match = re.search(

        r'i live in\s+([a-zA-Z\s]+)',

        text,

        re.IGNORECASE
    )

    if city_match:

        result[
            "city"
        ] = (

            city_match
            .group(1)

            .strip()

            .title()
        )

    # ---------------------------------
    # INCOME
    # ---------------------------------

    income_match = re.search(

        r'(\d+)\s*(lakh|lakhs|thousand|crore|crores)?',

        text,

        re.IGNORECASE
    )

    if income_match:

        result[
            "income"
        ] = (

            income_match
            .group(0)

            .strip()
        )

    # ---------------------------------
    # RETURN
    # ---------------------------------

    return result
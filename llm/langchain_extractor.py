import re



def extract_entities(text):

    entities = {}

    text_lower = text.lower()

    print("USER:", text)

    

    if "my name is" in text_lower:

        name = (
            text_lower
            .replace("my name is", "")
            .strip()
        )

        entities["full_name"] = (
            name.title()
        )

    # -----------------------------------
    # DOB
    # -----------------------------------

    dob_match = re.search(

        r"\d{2}[/-]\d{2}[/-]\d{4}",

        text
    )

    if dob_match:

        entities["dob"] = (
            dob_match.group()
        )

    # -----------------------------------
    # PAN
    # -----------------------------------

    pan_match = re.search(

        r"[A-Z]{5}[0-9]{4}[A-Z]",

        text.upper()
    )

    if pan_match:

        entities["pan"] = (
            pan_match.group()
        )

    # -----------------------------------
    # EMAIL
    # -----------------------------------

    email_match = re.search(

        r'[\w\.-]+@[\w\.-]+',

        text
    )

    if email_match:

        entities["email"] = (
            email_match.group()
        )

    # -----------------------------------
    # MOBILE
    # -----------------------------------

    mobile_match = re.search(

        r"\d{10}",

        text
    )

    if mobile_match:

        entities["mobile"] = (
            mobile_match.group()
        )

    print(
        "EXTRACTED:",
        entities
    )

    return entities
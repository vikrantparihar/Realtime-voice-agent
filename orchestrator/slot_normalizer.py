def normalize_extracted_entities(entities):

    normalized = {}

    mapping = {
        "name": "full_name",
        "full_name": "full_name",
        "dob": "dob",
        "date_of_birth": "dob",
        "pan": "pan",
        "address": "address",
        "email": "email",
        "mobile": "mobile"
    }

    for k, v in entities.items():

        key = mapping.get(k.lower())

        if key:
            normalized[key] = v

    return normalized
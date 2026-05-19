def merge_slots(session, entities):

    updated = False

    for key, value in entities.items():

        if key in session["slots"]:

            # only update if empty
            if not session["slots"][key]["value"]:
                session["slots"][key]["value"] = value
                updated = True

    return updated
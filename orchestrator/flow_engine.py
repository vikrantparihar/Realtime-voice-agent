class FlowEngine:

    def __init__(self, session):

        self.session = session

        self.questions = [
            "full_name",
            "dob",
            "pan",
            "address",
            "email",
            "mobile number",
            "father_name",
            "occupation",
            "city",
            "income"
        ]

        # STRICT POINTER (NO SKIP)
        self.index = session.get("current_question_index", 0)

    # ----------------------------
    # CURRENT QUESTION
    # ----------------------------

    def current(self):

        if self.index >= len(self.questions):
            return None

        return self.questions[self.index]

    # ----------------------------
    # STRICT VALIDATION
    # ----------------------------

    def can_fill(self, key):

        return key == self.current()

    # ----------------------------
    # FILL SLOT ONLY IF VALID
    # ----------------------------

    def fill(self, entities):

        current_key = self.current()

        filled = {}

        # ONLY CURRENT QUESTION ACCEPTED
        if current_key in entities:
            filled[current_key] = entities[current_key]

        return filled

    # ----------------------------
    # ADVANCE FLOW
    # ----------------------------

    def advance(self):

        self.index += 1
        self.session["current_question_index"] = self.index

    # ----------------------------
    # PROCESS STEP
    # ----------------------------

    def process(self, entities):

        result = self.fill(entities)

        if result:
            self.advance()

        return result
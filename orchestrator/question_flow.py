from orchestrator.bank_questions import QUESTIONS

class QuestionFlow:

    def __init__(self):
        self.current_question = 0

    def get_current_question(self):
        return QUESTIONS[self.current_question]

    def next_question(self):
        if self.current_question < len(QUESTIONS) - 1:
            self.current_question += 1

        return QUESTIONS[self.current_question]

    def is_complete(self):
        return self.current_question >= len(QUESTIONS) - 1
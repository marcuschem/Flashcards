import re


class FlashCard:

    def __init__(self, term: str, definition: str, counter: int):
        self.term = term
        self.definition = definition
        self.counter = 0

    def studying(self, answer: str) -> bool:
        if re.match(self.definition, answer):
            return True
        self.counter += 1
        return False

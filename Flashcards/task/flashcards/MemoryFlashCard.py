import os.path
import pickle
from FlashCard import FlashCard


class MemoryFlashCard:

    def __init__(self):
        self.dict_cards = {}

    def get_dict(self):
        return self.dict_cards

    def verify_card(self, term: str) -> bool:
        return term in self.dict_cards

    def verify_definition(self, definition: str) -> bool:
        for key, value in self.dict_cards.items():
            if value.definition == definition:
                return True
        return False

    def add_card(self, term: str, definition: str) -> None:
        new_card = FlashCard(term, definition, 0)
        self.dict_cards[new_card.term] = new_card

    def delete_card(self, selected_term: str) -> bool:
        for key, value in self.dict_cards.items():
            if key == selected_term:
                del self.dict_cards[key]
                return True
        return False

    def reset(self):
        for key, value in self.dict_cards.items():
            self.dict_cards[key] = FlashCard(key, value, 0)

    def save_on_json(self, file_name: str) -> int:
        with open(file_name, "wb") as file_:
            pickle.dump(self.dict_cards, file_)
        return len(self.dict_cards)

    def load_from_json(self, file_name: str) -> int or bool:
        if os.path.isfile(file_name):
            with open(file_name, "rb") as file_:
                loaded_dict = pickle.load(file_)
            for key, value in loaded_dict.items():
                if isinstance(value, FlashCard):
                    continue
                else:
                    del loaded_dict[key]
            loaded_dict.update(self.dict_cards)
            self.dict_cards.update(loaded_dict)
            return len(loaded_dict)
        return False

    def hardest_cards(self) -> list:
        list_max = []
        for key, value in self.dict_cards.items():
            list_max.append(value.counter)
        try:
            max_of_mistakes = max(list_max)
        except ValueError:
            return []
        else:
            return [value for value in self.dict_cards.values() if (value.counter == max_of_mistakes and value.counter > 0)]

    def display_cards(self, cards_for_playing: int):
        list_display = []
        dict_to_play = self.dict_cards.copy()
        for _ in range(cards_for_playing):
            try:
                list_display.append(dict_to_play.popitem())
            except KeyError:
                dict_to_play = self.dict_cards.copy()
                list_display.append(dict_to_play.popitem())
        for element in list_display:
            yield element

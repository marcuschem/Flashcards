import argparse
import sys
from MemoryFlashCard import MemoryFlashCard


class Menu:

    def __init__(self):
        self.cards = MemoryFlashCard()
        self.actions = ["add",
                        "remove",
                        "ask",
                        "exit",
                        "import",
                        "export",
                        "log",
                        "hardest card",
                        "reset stats"]
        self.buffer = []
        self._main_menu()

    def _is_action(self, action: str) -> bool:
        return action in self.actions

    def _append_to_buffer(self, argument: str) -> str:
        self.buffer.append(argument)
        return str(argument)

    def _add_card(self):
        print(self._append_to_buffer("The card:"))
        term = self._append_to_buffer(input())
        boolean = self.cards.verify_card(term)
        while boolean:
            print(self._append_to_buffer('This card already exists. Try again:'))
            term = self._append_to_buffer(input())
            boolean = self.cards.verify_card(term)
        print(self._append_to_buffer("The definition from card:"))
        definition = self._append_to_buffer(input())
        boolean = self.cards.verify_definition(definition)
        while boolean:
            print(self._append_to_buffer('This definition already exists. Try again:'))
            definition = self._append_to_buffer(input())
            boolean = self.cards.verify_definition(definition)
        self.cards.add_card(term, definition)
        print(self._append_to_buffer(f'("{term}", "{definition}") has been added'))

    def _remove_card(self) -> None:
        print(self._append_to_buffer("which card?"))
        term = self._append_to_buffer(input())
        boolean = self.cards.delete_card(term)
        if not boolean:
            print(self._append_to_buffer(f'Can\'t remove "{term}": there is no such card.'))
        else:
            print(self._append_to_buffer("The card has been removed"))

    def _importing(self, file_name) -> None:
        number_of_cards = self.cards.load_from_json(file_name)
        if number_of_cards:
            print(self._append_to_buffer(f"{number_of_cards} cards have been loaded."))
        else:
            print(self._append_to_buffer("File not found"))

    def _exporting(self, file_name2) -> None:
        number_of_cards = self.cards.save_on_json(file_name2)
        print(self._append_to_buffer(f"{number_of_cards} cards have been saved"))

    def _hardest_card(self) -> None:
        str_ = "The hardest cards are"
        list_records = self.cards.hardest_cards()
        if len(list_records) == 0:
            print(self._append_to_buffer("There are no cards with errors"))
        if len(list_records) == 1:
            term = list_records[-1].term
            number = list_records[-1].counter
            print(self._append_to_buffer(f'The hardest card is "{term}". You have {number} errors answering it.'))
        else:
            for element in list_records:
                str_ += ' "{}"'.format(element.term)
            print(self._append_to_buffer(str_))

    def _reset_stats(self):
        self.cards.reset()
        print(self._append_to_buffer("Card statistics have been reset."))

    def _display_cards(self) -> None:
        correct_term = ""
        print(self._append_to_buffer("How many times to ask?"))
        try:
            number_of_cards = int(input())
        except ValueError:
            sys.exit()
        self._append_to_buffer(str(number_of_cards))
        card_generator = self.cards.display_cards(number_of_cards)
        while True:
            try:
                card = next(card_generator)
                print(self._append_to_buffer(f'print the definition of "{card[-1].term}"'))
                answer = self._append_to_buffer(input())
                for key, value in self.cards.get_dict().items():
                    if answer == value.definition:
                        correct_term += key
                study = card[-1].studying(answer)
                if study:
                    print(self._append_to_buffer("Correct!"))
                elif not study and correct_term:
                    print(self._append_to_buffer(f'Wrong. The right answer is "{card[-1].definition}", but your definition is correct for "{correct_term}"'))
                else:
                    print(self._append_to_buffer(f'Wrong. The right answer is "{card[-1].definition}"'))
            except StopIteration:
                break

    def _log(self) -> None:
        print(self._append_to_buffer("File name:"))
        file_ = self._append_to_buffer(input())
        with open(file_, "a", encoding="UTF-8") as my_log:
            for element in self.buffer:
                print(element, file=my_log, flush=True)
        self.buffer.clear()
        print(self._append_to_buffer("The log has been saved."))

    def _main_menu(self) -> None:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument("-i", "--import_from")
        parser.add_argument("-e", "--export_to")
        args = parser.parse_args()
        if args.import_from:
            self._importing(args.import_from)
        action = ""
        while action != "exit":
            print(self._append_to_buffer("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"))
            action = self._append_to_buffer(input())
            if self._is_action(action):
                if action == "add":
                    self._add_card()
                elif action == "remove":
                    self._remove_card()
                elif action == "import":
                    print(self._append_to_buffer("File name:"))
                    file_ = self._append_to_buffer(input())
                    self._importing(file_)
                elif action == "export":
                    print(self._append_to_buffer("File name:"))
                    file_ = self._append_to_buffer(input())
                    self._exporting(file_)
                elif action == "ask":
                    self._display_cards()
                elif action == "hardest card":
                    self._hardest_card()
                elif action == "reset stats":
                    self._reset_stats()
                elif action == "log":
                    self._log()
                else:
                    if args.export_to:
                        self._exporting(args.export_to)
                    print(self._append_to_buffer("Bye bye!"))
                    sys.exit()
            else:
                if args.export_to:
                    self._exporting(args.export_to)
                sys.exit()
            print(self._append_to_buffer("\n"))

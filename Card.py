class Card:

    def __init__(self, name: str, value: int, suit: int):
        self.name = name
        self.value = value
        self.suit = suit

    def print_card(self):
        print(self.name)

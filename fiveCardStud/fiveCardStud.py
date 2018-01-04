from deuces.deuces import Deck


class FiveCardStud:
    def __init__(self):
        self.game_number = 0
        self.decks = []
        self.new_game()

    def set_game_numer(self, new_number):
        self.game_number = new_number

    def get_game_number(self):
        return self.game_number

    def new_game(self, deck_number=1):
        decks = []
        for i in range(deck_number):
            decks.extend(Deck.GetFullDeck())
        return decks
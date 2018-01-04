from src.modules.game.game import Game
from src.modules.deuces.deck import Deck


class FiveCardStud(Game):
    def __init__(self):
        super().__init__()
        self.game_name = "Five Card Stud"

    def new_game(self, deck_number=1):
        decks = []
        for i in range(deck_number):
            decks.extend(Deck.GetFullDeck())
        return decks

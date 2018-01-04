from src.modules.game.game import Game
from src.modules.deuces.deck import Deck
from src.modules.player.five_card_stud_player import FiveCardStudPlayer


class FiveCardStud(Game):
    def __init__(self, player_limit):
        super().__init__()
        self.game_name = "Five Card Stud"
        self.deck = None
        self.players = {}
        self.player_limit = player_limit

    def new_game(self, number_of_player):
        self.decks = Deck()
        for i in range(number_of_player):
            self.players[i] = FiveCardStudPlayer(i)

    def add_player(self):
        if len(self.players) < self.player_limit:
            for i in range(self.player_limit):
                if not self.players.get(i, None):
                    self.players[i] = FiveCardStudPlayer(i)
                    break
        else:
            print("Cannot add player. Number of players reach limit")

    def remove_player(self, player_id):
        if self.players.get(player_id, None):
            del self.players[player_id]
        else:
            print("Cannot remove player, id: %d player doesn't exist" % player_id)



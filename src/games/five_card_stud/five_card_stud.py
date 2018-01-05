from src.modules.game.game import Game
from src.modules.deuces.deck import Deck
from src.modules.player.five_card_stud_player import FiveCardStudPlayer
from src.modules.game.money_pool import MoneyPool
from random import randint


class FiveCardStud(Game):

    def __init__(self, player_limit=2):
        super().__init__()
        self.game_name = "Five Card Stud"
        self.deck = None
        self.players = {}
        self.player_limit = player_limit
        self.to_play = None
        self.current_bet = 0
        self.round_count = 0
        self.money_pool = MoneyPool()
        self.attend_players = []
        self.commands = {
            "call": self.call,
            "raise": self.raise_bet,
            "fold": self.fold,
            "check": self.check,
            "bet": self.bet,
            "showhand": self.show_hand,
        }

    def new_game(self, number_of_player):
        self.decks = Deck()
        for i in range(number_of_player):
            self.players[i] = FiveCardStudPlayer(i)

    def add_player(self):
        # add new player into spare spot
        if len(self.players) < self.player_limit:
            for i in range(self.player_limit):
                if not self.players.get(i, None):
                    self.players[i] = FiveCardStudPlayer(i)
                    break
        else:
            print("Cannot add player. Number of players reach limit: %d players" % self.player_limit)

    def remove_player(self, player_id):
        if self.players.get(player_id, None):
            del self.players[player_id]
        else:
            print("Cannot remove player, id: %d player doesn't exist" % player_id)

    def play(self):
        game_over = False
        round = 0
        attend_players = []
        for i in range(len(self.players)):
            attend_players.append(self.players.get(i))
        current_pos = randint(0, len(attend_players) - 1)
        if len(attend_players) < 2:
            print("No enough players, Only %d playes attend" % len(attend_players) )
            return
        # self.current_player = attend_players.pop(current_pos)
        while not game_over:
            round += 1
            self.to_play = attend_players
            cmd = input("input command to play (currnet player: %d): " % self.current_player.get_player_id())

    def new_round(self):
        pass

    def call(self):
        pass

    def raise_bet(self, amount):
        pass

    def fold(self):
        pass

    def check(self):
        pass

    def bet(self, amount):
        pass

    def show_hand(self):
        pass



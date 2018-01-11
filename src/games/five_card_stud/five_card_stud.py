from src.modules.game.game import Game
from src.modules.deuces.deck import Deck
from src.modules.deuces.card import Card
from src.modules.deuces.evaluator import Evaluator
from src.modules.player.five_card_stud_player import FiveCardStudPlayer
from src.modules.game.money_pool import MoneyPool


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
        self.raise_count = [x[:] for x in [[False] * (self.player_limit + 1)] * 6]
        self.money_pool = MoneyPool()
        self.alive_players = []
        self.commands = {
            "call": self._call_cmd,
            "raise": self._raise_cmd,
            "fold": self._fold_cmd,
            "check": self._check_cmd,
            "bet": self._bet_cmd,
            "showhand": self._showhand_cmd,
        }

    def new_game(self, number_of_player):
        self.deck = Deck()
        self.players = {}
        for i in range(number_of_player):
            self.players[i] = FiveCardStudPlayer(i)
        self.alive_players.clear()
        self.money_pool = MoneyPool()
        self.round_count = 0
        self.raise_count = [x[:] for x in [[False] * (self.player_limit + 1)] * 6]

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
        winner = None
        for i in range(len(self.players)):
            self.alive_players.append(self.players.get(i))

        # current_pos = randint(0, len(alive_players) - 1)
        if len(self.alive_players) < 2:
            print("No enough players, Only %d playes attend" % len(self.alive_players))
            return

        # draw one card for each player before start
        self.draw_cards(1)
        while len(self.alive_players) > 1 and self.round_count < 5:
            self.round_count += 1
            self.remove_giveup_players()
            self.draw_cards(1)
            for self.to_play in self.round():
                cmd= input("input command to play (currnet player: %d) and amount if needed: "
                           % self.to_play.get_player_id())
                self.commands.get(cmd, self._default_cmd)()

        # Evaluate all alive players cards, find the winner
        if self.round_count < 5 and len(self.alive_players) == 1:
            winner = self.alive_players[0]
        elif self.round_count == 5 and len(self.alive_players) > 1:
            winner = self.find_winner()
        else:
            print("Cannot find a winner for this game, ")
        if winner:
            print(winner.get_player_id())
        exit(0)

    def round(self):
        round_players = self.alive_players[:]
        pos = self.find_high_card_player().get_player_id()
        count = 0

        while count < len(round_players):
            count += 1
            if self.raise_count[self.round_count][round_players[pos].get_player_id]:
                return
            if not round_players[pos].get_give_up():
                yield round_players[pos]
                if self.raise_count[self.round_count][round_players[pos].get_player_id]:
                    count = 1
                    pos = round_players.index(round_players[pos])
            pos -= 1


        # for i in range(len(round_players)):
        #     if not round_players[i].get_give_up():
        #         yield round_players[pos]
        #     pos -= 1

    def _call_cmd(self, _):
        if self.current_bet == 0:
            return True
        else:
            print("cannot call if other players bet something")
            return False

    def _raise_cmd(self):
        amount = int(input("please input amount for raise"))
        to_bet = amount + self.current_bet
        if to_bet > self.to_play.get_carry_money():
            print("You cannot bet that much, you want to bet %d but you only have %d!" % (to_bet, self.to_play.get_carry_money()))
            return False
        else:
            self.money_pool.add(self.to_play.withdraw_money(to_bet), self.to_play.get_player_id())
            self.current_bet = to_bet
            return True

    def _fold_cmd(self):
        self.to_play.set_give_up(True)
        return True

    def _check_cmd(self):
        to_bet = self.current_bet
        if to_bet > self.to_play.get_carry_money():
            print("You cannot check, you only have %d!" % self.to_play.get_carry_money())
            return False
        else:
            self.money_pool.add(self.to_play.withdraw_money(to_bet), self.to_play.get_player_id())
            return True

    def _bet_cmd(self, player, amount):
        pass

    def _showhand_cmd(self, player, amount):
        pass

    def _default_cmd(self, player):
        print("Unknow command!")

    def is_greater_than(self, card1, card2):
        """
        Check if card 1 is greater than card 2, based on rank and suit
        :param card1:
        :param card2:
        :return:
        """
        prime1 = Card.get_prime(card1)
        suit1 = Card.get_suit_int(card1)
        prime2 = Card.get_prime(card2)
        suit2 = Card.get_suit_int(card2)

        if prime1 == prime2:
            if suit1 == suit2:
                print("Two cards are equal")
                return False
            else:
                return True if suit1 < suit2 else False
        else:
            return True if prime1 > prime2 else False

    def find_high_card_player(self):
        """
        If there any player is still alive in the game, return the player who has the highest card that is last assigned
        :return:
        """
        if len(self.alive_players) == 0:
            print("No player is still alive in the game")
            return None
        high_card_player = self.alive_players[0]
        for player in self.alive_players:
            if self.is_greater_than(player.get_hand()[-1], high_card_player.get_hand()[-1]):
                high_card_player = player
        return high_card_player

    def draw_cards(self, number_of_card):
        for player in self.alive_players:
            if number_of_card == 1:
                player.add_to_hand([self.deck.draw(number_of_card)])
            else:
                player.add_to_hand(self.deck.draw(number_of_card))

    def find_winner(self):
        """
        Find a winner in the alive players
        :return:
        """
        if len(self.alive_players) == 0:
            print("No player is alive at the end of game")
            return None
        elif len(self.alive_players) == 1:
            return self.alive_players[0]
        else:
            winner = self.alive_players[0]
            evaluator = Evaluator()
            for player in self.alive_players:
                if evaluator.evaluate(player.get_hand, []) < evaluator.evaluate(winner.get_hand, []):
                    winner = player
            return winner

    def remove_giveup_players(self):
        alive_players = []
        for player in self.alive_players:
            if not player.get_give_up():
                alive_players.append(player)
        self.alive_players = alive_players

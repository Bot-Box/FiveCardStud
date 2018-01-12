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
        self.last_raised_player = None
        self.money_pool = MoneyPool()
        self.alive_players = []
        self.commands = {
            "call": self._call_cmd,
            "raise": self._raise_cmd,
            "fold": self._fold_cmd,
            "check": self._check_cmd,
            "bet": self._bet_cmd,
            "showhand": self._showhand_cmd,
            "info": self._info_cmd,
        }

    def new_game(self, number_of_player):
        self.deck = Deck()
        self.players = {}
        for i in range(number_of_player):
            self.players[i] = FiveCardStudPlayer(i)
        self.alive_players.clear()
        self.money_pool = MoneyPool()
        self.round_count = 0
        self.last_raised_player = None

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

        # continue game if there are more than one player in the game and player has
        while len(self.alive_players) > 1 and self.round_count < 4:
            self.round_count += 1
            self.draw_cards(1)
            self.current_bet = 0
            for self.to_play in self.round():
                while True:
                    cmd = input("input command to play (currnet player: %d): "
                                % self.to_play.get_player_id())
                    if self.commands.get(cmd, self._default_cmd)():
                        break
            self.remove_gaveup_players()

        # Evaluate all alive players cards, find the winner
        if self.round_count < 4 and len(self.alive_players) == 1:
            winner = self.alive_players[0]
        elif self.round_count == 4 and len(self.alive_players) > 1:
            winner = self.find_winner()
        else:
            print("Cannot find a winner for this game, ")
        if winner:
            print("Winner is: %d" % winner.get_player_id())
        exit(0)

    def round(self):
        round_players = self.alive_players[:]
        pos = self.find_high_card_player().get_player_id()
        self.last_raised_player = None
        give_up_count = 0

        count = 0
        while count < len(round_players):
            count += 1
            player = round_players[pos]
            # If this player didn't give up, let it choose actions
            if not player.get_give_up():
                yield player
                if player.get_give_up():
                    give_up_count += 1
                    # Check if there is only one player alive
                    if give_up_count == len(round_players) - 1:
                        return
                # After this player action, if he is the last player raised bet, then reset the count
                if self.last_raised_player == player.get_player_id():
                    count = 1
                    pos = round_players.index(player)
            pos -= 1

    def _check_cmd(self):
        if self.current_bet != 0:
            print("cannot check if other players bet something")
            return False
        else:
            return True

    def _raise_cmd(self):
        if self.to_play.get_raised():
            print("You already raised, please use call or fold")
            return False
        amount = int(input("please input amount for raise"))
        to_bet = amount + self.current_bet
        if to_bet > self.to_play.get_carry_money():
            print("You cannot bet that much, you want to bet %d but you only have %d!" % (to_bet, self.to_play.get_carry_money()))
            return False
        elif self.to_play.get_raised():
            print("You already raised, you only can do call or fold")
            return False
        else:
            self.money_pool.add(self.to_play.withdraw_money(to_bet), self.to_play.get_player_id())
            self.current_bet = to_bet
            self.last_raised_player = self.to_play.get_player_id()
            return True

    def _fold_cmd(self):
        self.to_play.set_give_up(True)
        return True

    def _call_cmd(self):
        to_bet = self.current_bet
        if to_bet > self.to_play.get_carry_money():
            print("You cannot call, you only have %d!" % self.to_play.get_carry_money())
            return False
        else:
            self.money_pool.add(self.to_play.withdraw_money(to_bet), self.to_play.get_player_id())
            return True

    def _bet_cmd(self):
        if self.to_play.get_raised():
            print("You already raised, please use call or fold")
            return False
        amount = int(input("please input amount for bet"))
        to_bet = amount
        if to_bet > self.to_play.get_carry_money():
            print("You cannot bet that much, you want to bet %d but you only have %d!" % (
            to_bet, self.to_play.get_carry_money()))
            return False
        elif self.to_play.get_raised():
            print("You already raised, you only can do call or fold")
            return False
        else:
            self.money_pool.add(self.to_play.withdraw_money(to_bet), self.to_play.get_player_id())
            self.current_bet = to_bet
            self.last_raised_player = self.to_play.get_player_id()
            return True

    def _showhand_cmd(self):
        pass

    def _default_cmd(self):
        print("Unknow command!")

    def _info_cmd(self):
        print("Money pool has: %d" % self.money_pool.get_total_money())
        for _, player in self.players.items():
            print("Player: %d, Carry money: %d, hand:" % (player.get_player_id(), player.get_carry_money()))
            Card.print_pretty_cards(player.get_hand())
            print("---------")
        return False



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
                # print("Two cards are equal")
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
            if not player.get_give_up() and self.is_greater_than(player.get_hand()[-1], high_card_player.get_hand()[-1]):
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
                if evaluator.evaluate(player.get_hand(), []) < evaluator.evaluate(winner.get_hand(), []):
                    winner = player
            return winner

    def remove_gaveup_players(self):
        alive_players = []
        for player in self.alive_players:
            if not player.get_give_up():
                alive_players.append(player)
        self.alive_players = alive_players

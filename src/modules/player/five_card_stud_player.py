from .player import Player


class FiveCardStudPlayer(Player):
    """
    This is the object of player who will play five card stud
    """
    def __init__(self, player_id):
        super().__init__(player_id)
        self.carry_money = 0
        self.hand = []

    def add_carry_money(self, amount):
        self.carry_money += amount

    def get_carry_money(self):
        return self.carry_money

    def clear_carry_money(self):
        self.carry_money = 0

    def add_to_hand(self, cards):
        self.hand.extend(cards)

    def get_hand(self):
        return self.hand

from .player import Player


class FiveCardStudPlayer(Player):
    """
    This is the object of player who will play five card stud
    """
    def __init__(self, player_id):
        super().__init__(player_id)
        self.carry_money = 1000
        self.hand = []
        self.is_give_up = False
        self.raised = False

    def add_carry_money(self, amount):
        self.carry_money += amount

    def withdraw_money(self, amount):
        if self.carry_money < amount:
            print("You don't have enough money to withdraw!")
            return 0
        else:
            self.carry_money -= amount
            return self.carry_money

    def get_carry_money(self):
        return self.carry_money

    def clear_carry_money(self):
        self.carry_money = 0

    def add_to_hand(self, cards):
        self.hand.extend(cards)

    def get_hand(self):
        return self.hand

    def set_give_up(self, give_up):
        self.is_give_up = give_up

    def get_give_up(self):
        return self.is_give_up

    def set_raised(self, raised):
        self.raised = raised

    def get_raised(self):
        return self.raised
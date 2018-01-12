class MoneyPool:
    def __init__(self):
        self.money = {}
        self.total_money = 0

    def add(self, amount, player_id):
        self.total_money += amount
        if not self.money.get(player_id, None):
            self.money[player_id] = [amount]
        else:
            self.money[player_id].append(amount)

    def get(self, player_id):
        return self.money.get(player_id, 0)

    def clear(self):
        self.money.clear()
        self.total_money = 0

    def withdraw_all(self):
        money = self.total_money
        self.clear()
        return money

    def get_total_money(self):
        return self.total_money

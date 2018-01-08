from src.modules.deuces import Deck


class Game:
    def __init__(self):
        self.game_number = 0
        self.game_name = "Game"

    def set_game_numer(self, new_number):
        self.game_number = new_number

    def get_game_number(self):
        return self.game_number

    def set_game_name(self, new_game_name):
        self.game_name = new_game_name

    def get_game_name(self):
        return self.game_name
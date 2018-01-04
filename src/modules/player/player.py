#!/usr/bin/python3


class Player:
    def __init__(self):
        """
        player module
        :param self:
        :return:
        """
        self.name = "Default Player"
        self.player_number = 0

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def set_player_number(self, new_number):
        self.player_number = new_number

    def get_number(self):
        return self.player_number


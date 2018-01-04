#!/usr/bin/python3


class Player:
    def __init__(self, player_id=1):
        """
        Basic player module
        :param self:
        :return:
        """
        self.name = "Default Player"
        self.player_id = player_id

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def set_player_id(self, new_id):
        self.player_id = new_id

    def get_player_id(self):
        return self.player_id


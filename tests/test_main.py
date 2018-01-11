from src.modules.player.five_card_stud_player import FiveCardStudPlayer
from src.modules.deuces.card import Card
from src.modules.deuces.evaluator import Evaluator
from src.games.five_card_stud.five_card_stud import FiveCardStud

player1 = FiveCardStudPlayer(1)

# print(player1.get_player_id())


dict1 = {}
dict1[0] = 1
dict1[0] += 1

# print(dict1[0])


raise_count = [x[:] for x in [[False] * 3] * 6]
print(raise_count)
round_count = 3


def round(alive_players):
    round_players = alive_players[:]
    pos = 0
    count = 0

    while count < len(round_players):
        count += 1
        if raise_count[round_count][round_players[pos].get_player_id()]:
            return
        if not round_players[pos].get_give_up():
            yield round_players[pos]
            if raise_count[round_count][round_players[pos].get_player_id()]:
                count = 1
                pos = round_players.index(round_players[pos])
        pos -= 1

a = [FiveCardStudPlayer(1), FiveCardStudPlayer(2)]


for player in round(a):
    raise_count[3][player.get_player_id()] = True
    print(player.get_player_id())

# for i in round(a, 2):
    # print(i)

card1 = Card.new("Ad")
card2 = Card.new("3s")


def is_greater_than(card1, card2):
    """
    Check if card 1 is greater than card 2
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


# print(is_greater_than(card1, card2))


def test():
    print("okay")

def default():
    print("not okay")

commands = {
        "call": test,
        "default": default,
    }

commands.get("calls", default)()


card1 = Card.new("As")
card2 = Card.new("Ac")
card3 = Card.new("4d")
card4 = Card.new("5d")
card5 = Card.new("6d")

hand1 = [card1, card2, card3, card4, card5]

card6 = Card.new("Ah")
card7 = Card.new("2d")
card8 = Card.new("3s")
card9 = Card.new("4s")
card10 = Card.new("5s")

hand2 = [card6, card7, card8, card9, card10]

evaluator = Evaluator()

print(evaluator.evaluate(hand1, []))
print(evaluator.evaluate(hand2, []))


# a = [1,2,3,4]

# print(a[-7])

# game = FiveCardStud()
# game.new_game(2)
# game.play()
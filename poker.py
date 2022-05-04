

class PokerGame(object):
    """
    emulates a game of poker
    """

    def __init__(self, players):
        """
        input parameter:    players
        data type:          list[Player (local class)]
        description:        object that represents a player in the game
        """
        self.players = players


class TexasHoldEm(PokerGame):
    """
    game of no-limit Texas Hold 'em
    """

    def __init__(self, players, limit=0):
        """
        input parameter:    limit
        data type:          integer
        description:        maximum bet per player in a hand
        """
        super().__init__(players)
        self.cards_dealt = 2
        self.limit = limit


class Player(object):
    """
    emulates a player in a game of poker
    """

    def __init__(self, name, chips):
        """
        input parameter:    name
        data type:          string
        description:        identity of the player
        """
        self.name = name
        self.chips = chips


if __name__ == '__main__':

    player_names = ['p1', 'p2', 'p3', 'p4']
    the_guys = []
    for guy in the_guys:
        the_guys.append(Player(guy, 10000))

    TexasHoldEm(the_guys)

import random


class PokerGame(object):
    """
    emulates a game of poker (tournament)
    """

    def __init__(self, players):
        """
        input parameter:    players
        data type:          list[Player (local class)]
        description:        object that represents a player in the game
        """
        self.players = players
        self.deck = []
        self.__make_deck()
        self.player_count = len(players)

    def __make_deck(self):
        suits = ['s', 'c', 'h', 'd']
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'j', 'q', 'k', 'a']
        for suit in suits:
            for card in cards:
                self.deck.append(card + suit)
        self.shuffle()

    def shuffle(self):
        for player in self.players:
            player.muck_hand()
        random.shuffle(self.deck)

    def seat_players(self):
        seat = 0
        for player in self.players:
            player.set_seat(seat)
            seat += 1

    def __check_stacks(self):
        for index, player in enumerate(self.players):
            if player.chips == 0:
                self.players.pop(index)
                for subsequent_players in self.players:
                    subsequent_players.seat -= 1
                self.player_count -= 1


class HoldEmPot(object):
    """
    emulates the pot of a poker game
    """

    def __init__(self):
        self.pre_flop = {}
        self.pre_turn = {}
        self.pre_river = {}
        self.post_river = {}
        self.pot_size = 0

    def bet_pre_flop(self, gambler, chips):
        if gambler in self.pre_flop:
            self.pre_flop[gambler] += chips
        else:
            self.pre_flop[gambler] = chips
        self.pot_size += chips

    def bet_pre_turn(self, gambler, chips):
        if gambler in self.pre_turn:
            self.pre_turn[gambler] += chips
        else:
            self.pre_turn[gambler] = chips
        self.pot_size += chips

    def bet_pre_river(self, gambler, chips):
        if gambler in self.pre_river:
            self.pre_river[gambler] += chips
        else:
            self.pre_river[gambler] = chips
        self.pot_size += chips

    def bet_post_river(self, gambler, chips):
        if gambler in self.post_river:
            self.post_river[gambler] += chips
        else:
            self.post_river[gambler] = chips
        self.pot_size += chips

    def divvy(self, rankings):
        for winner in rankings:
            if winner in self.pre_flop:
                winnings = self.pre_flop[winner]
                for gambler in self.pre_flop:
                    winner.add_chips(winnings)
                    self.pre_flop[gambler] -= winnings
                    self.pot_size -= winnings
            if winner in self.pre_turn:
                winnings = self.pre_turn[winner]
                for gambler in self.pre_turn:
                    winner.add_chips(winnings)
                    self.pre_turn[gambler] -= winnings
                    self.pot_size -= winnings
            if winner in self.pre_river:
                winnings = self.pre_river[winner]
                for gambler in self.pre_river:
                    winner.add_chips(winnings)
                    self.pre_river[gambler] -= winnings
                    self.pot_size -= winnings
            if winner in self.post_river:
                winnings = self.post_river[winner]
                for gambler in self.post_river:
                    winner.add_chips(winnings)
                    self.post_river[gambler] -= winnings
                    self.pot_size -= winnings
            if self.pot_size == 0:
                self.__reset()
                break

    def __reset(self):
        self.pre_flop = {}
        self.pre_turn = {}
        self.pre_river = {}
        self.post_river = {}


class TexasHoldEm(PokerGame):
    """
    game of Texas Hold 'em
    """

    def __init__(self, players, blinds, limit=0):
        """
        input parameter:    blinds
        data type:          list[integers]
        description:        index 0 is the starting small blind
                            index 1 is the starting big blind

        input parameter:    limit
        data type:          integer
        description:        maximum bet per player in a hand
        """
        super().__init__(players)
        self.cards_dealt = 2
        self.limit = limit
        self.comm_cards = []
        self.burn_pile = []
        self.dealer = -1
        self.small_blind = 0
        self.big_blind = 1
        self.__rotate_blinds()
        self.blinds = blinds
        self.pot = HoldEmPot()
        self.round = 'pre flop'

    def __rotate_blinds(self):
        if self.dealer + 1 == self.player_count:
            self.dealer = 0
        else:
            self.dealer += 1
        if self.dealer + 1 == self.player_count:
            self.small_blind = 0
        else:
            self.small_blind = self.dealer + 1
        if self.small_blind + 1 == self.player_count:
            self.big_blind = 0
        else:
            self.big_blind = self.small_blind + 1

    def make_bet(self, player, chips):
        if self.round == 'pre flop':
            self.pot.bet_pre_flop(player, player.bet(chips))
        elif self.round == 'pre turn':
            self.pot.bet_pre_turn(player, player.bet(chips))
        elif self.round == 'pre river':
            self.pot.bet_pre_river(player, player.bet(chips))
        elif self.round == 'post river':
            self.pot.bet_post_river(player, player.bet(chips))

    def deal_cards(self):
        self.round = 'pre flop'
        self.comm_cards = []
        self.burn_pile = []
        self.shuffle()
        for _ in range(self.cards_dealt):
            for player in self.players:
                player.deal_card(self.deck.pop(0))
        sb = self.players[self.small_blind]
        bb = self.players[self.big_blind]
        self.make_bet(sb, self.blinds[0])
        self.make_bet(bb, self.blinds[1])

    def flop(self):
        self.round = 'pre turn'
        self.burn_pile.append(self.deck.pop(0))
        for _ in range(3):
            card = self.deck.pop(0)
            self.comm_cards.append(card)
            for player in self.players:
                player.deal_card(card)

    def turn(self):
        self.round = 'pre river'
        self.burn_pile.append(self.deck.pop(0))
        card = self.deck.pop(0)
        self.comm_cards.append(card)
        for player in self.players:
            player.deal_card(card)

    def river(self):
        self.round = 'post river'
        self.burn_pile.append(self.deck.pop(0))
        card = self.deck.pop(0)
        self.comm_cards.append(card)
        for player in self.players:
            player.deal_card(card)

    def up_blinds(self, new_blinds):
        self.blinds = new_blinds


class Player(object):
    """
    emulates a player in a game of poker
    """

    def __init__(self, name, chips):
        """
        input parameter:    name
        data type:          string
        description:        identity of the player

        input parameter:    chips
        data type:          integer
        description:        quantity of chips player starts with
        """
        self.name = name
        self.chips = chips
        self.hand = []
        self.seat = -1

    def bet(self, val):
        if val > self.chips:
            bet = self.chips
            self.chips = 0
            return bet
        else:
            self.chips -= val
            return val

    def add_chips(self, val):
        self.chips += val

    def chip_count(self):
        return self.chips

    def muck_hand(self, show=False):
        if show:
            print(self.hand)
        self.hand = []

    def deal_card(self, card):
        self.hand.append(card)

    def set_seat(self, seat_num):
        self.seat = seat_num


if __name__ == '__main__':

    player_names = ['p1', 'p2', 'p3', 'p4']
    the_guys = []
    for guy in player_names:
        the_guys.append(Player(guy, 10000))

    guys_game = TexasHoldEm(the_guys, [50, 100])
    guys_game.deal_cards()
    print(guys_game.pot.pot_size)
    guys_game.flop()
    guys_game.turn()
    guys_game.river()

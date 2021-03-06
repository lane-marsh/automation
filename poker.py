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
        cards = ['a', 'k', 'q', 'j', '0', '9', '8', '7', '6', '5', '4', '3', '2']
        for suit in suits:
            for card in cards:
                self.deck.append(card + suit)
        self.shuffle()

    def shuffle(self):
        for player in self.players:
            player.fold()
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

    def evaluate(self):
        rankings = []
        still_in = []
        for player in self.players:
            if player.in_hand:
                still_in.append(player)

        cards = ['a', 'k', 'q', 'j', '0', '9', '8', '7', '6', '5', '4', '3', '2', 'a']

        # straight flush check
        for index in range(10):
            c1 = cards[index]
            c2 = cards[index + 1]
            c3 = cards[index + 2]
            c4 = cards[index + 3]
            c5 = cards[index + 4]
            match = []
            for player in still_in:
                this_hand = player.hand
                suit = ''
                for card in this_hand:
                    if card[0] == c1:
                        suit = card[1]
                if suit != '':
                    if c2 + suit in this_hand and \
                       c3 + suit in this_hand and \
                       c4 + suit in this_hand and \
                       c5 + suit in this_hand:
                        match.append(player)
                        still_in.remove(player)
            if match:
                rankings.append(match)

        # four of a kind check
        for number in cards:
            match = []
            match_4 = []
            for player in still_in:
                score = 0
                for card in player.hand:
                    if card[0] == number:
                        score += 1
                if score == 4:
                    match_4.append(player)
                    still_in.remove(player)
            if match_4:
                for kicker in cards:
                    match = []
                    for player_4 in match_4:
                        if kicker != number:
                            for card in player_4.hand:
                                if card[0] == kicker:
                                    match.append(player_4)
            if match:
                rankings.append(match)

        # full house check
        for number in cards:
            match = []
            match_3 = []
            for player in still_in:
                score3 = 0
                for card in player.hand:
                    if card[0] == number:
                        score3 += 1
                if score3 == 3:
                    match_3.append(player)
            if match_3:
                for kicker in cards:
                    match = []
                    for player_3 in match_3:
                        score2 = 0
                        if kicker != number:
                            for card in player_3.hand:
                                if card[0] == kicker:
                                    score2 += 1
                            if score2 >= 2:
                                print('full house', player_3)
                                match.append(player_3)
                                still_in.remove(player_3)
                    if match:
                        rankings.append(match)

        # flush check
        for number in cards:
            match = []
            for player in still_in:
                for card in player.hand:
                    if card[0] == number:
                        suit = card[1]
                        suit_count = 0
                        for check_suits in player.hand:
                            if check_suits[1] == suit:
                                suit_count += 1
                        if suit_count >= 5:
                            print('flush', player)
                            match.append(player)
                            still_in.remove(player)
            if match:
                rankings.append(match)

        # straight check
        for index in range(10):
            match = []
            for player in still_in:
                c1 = cards[index]
                c1_check = False
                c2 = cards[index + 1]
                c2_check = False
                c3 = cards[index + 2]
                c3_check = False
                c4 = cards[index + 3]
                c4_check = False
                c5 = cards[index + 4]
                c5_check = False
                this_hand = player.hand
                for card in this_hand:
                    if card[0] == c1:
                        c1_check = True
                    if card[0] == c2:
                        c2_check = True
                    if card[0] == c3:
                        c3_check = True
                    if card[0] == c4:
                        c4_check = True
                    if card[0] == c5:
                        c5_check = True
                if c1_check and c2_check and c3_check and c4_check and c5_check:
                    print('straight', player)
                    match.append(player)
                    still_in.remove(player)
            if match:
                rankings.append(match)

        # 3 of a kind check
        for number in cards:
            match = []
            match_3 = []
            for player in still_in:
                score3 = 0
                for card in player.hand:
                    if card[0] == number:
                        score3 += 1
                if score3 == 3:
                    print('3 of kind', player)
                    match_3.append(player)
                    still_in.remove(player)
            if match_3:
                for kicker1 in cards:
                    if kicker1 != number:
                        match_k1 = []
                        match_k2 = []
                        for player_1 in match_3:
                            for card in player_1.hand:
                                if card[0] == kicker1:
                                    match_k1.append(player_1)
                        if len(match_k1) > 1:
                            for kicker2 in cards:
                                if kicker2 != number and kicker2 != kicker1:
                                    for player_2 in match_k1:
                                        for card in player_2.hand:
                                            if card[0] == kicker2:
                                                match_k2.append(player_2)
                        if match_k2:
                            rankings.append(match_k2)
                        elif match_k1:
                            rankings.append(match_k1)

            if match:
                rankings.append(match)

        # 2 pair check
        # 2 of a kind check
        # high card check

        return rankings


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
        self.pot = self.Pot()
        self.round = 'pre flop'

    class Pot(object):
        """
        emulates the pot of a poker game
        """

        def __init__(self):
            self.contributions = {}
            self.pot_size = 0

        def bet(self, gambler, chips):
            if gambler in self.contributions:
                self.contributions[gambler] += chips
            else:
                self.contributions[gambler] = chips
            self.pot_size += chips

        def divvy(self, rankings):
            for rank in rankings:
                max_bet = 0
                for winner in rank:
                    if self.contributions[winner] > max_bet:
                        max_bet = self.contributions[winner]
                for winner in rank:
                    waged = self.contributions[winner]
                    winners = len(rank)
                    for player in self.contributions:
                        winnings = min(waged, self.contributions[player])
                        self.contributions[player] -= winnings
                        winner.add_chips(winnings / winners)
                        self.pot_size -= winnings

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
        self.pot.bet(player, player.bet(chips))

    def deal_cards(self):
        self.round = 'pre flop'
        self.comm_cards = []
        self.burn_pile = []
        self.shuffle()
        for _ in range(self.cards_dealt):
            for player in self.players:
                player.deal_card(self.deck.pop(0))
        for player in self.players:
            player.in_hand = True
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
        self.in_hand = False

    def __repr__(self):
        return self.name

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

    def fold(self, show=False):
        if show:
            print(self.hand)
        self.hand = []
        self.in_hand = False

    def deal_card(self, card):
        self.hand.append(card)

    def set_seat(self, seat_num):
        self.seat = seat_num


if __name__ == '__main__':

    player_names = ['p1', 'p2', 'p3', 'p4']
    p1 = Player('p1', 10000)
    p2 = Player('p2', 10000)
    p3 = Player('p3', 10000)
    p4 = Player('p4', 10000)
    the_guys = [p1, p2, p3, p4]

    guys_game = TexasHoldEm(the_guys, [50, 100])
    guys_game.deal_cards()
    guys_game.flop()
    guys_game.turn()
    guys_game.river()

    for guy in guys_game.players:
        print(guy.name, guy.chips)

    print(guys_game.evaluate())

    guys_game.pot.divvy([[p3], [p2]])

    for guy in guys_game.players:
        print(guy.name, guy.chips, guy.in_hand, guy.hand)

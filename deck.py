from card import Card
import random


class Deck(object):
    def __init__(self):
        self.cards = []
        for pips in range(1, 14):
            for suit in ["spades", "clubs", "diamonds", "hearts"]:
                self.cards.append(Card(pips, suit))
        self.shuffle()

    def deal(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None

    def is_empty(self):
        return len(self.cards) == 0

    def shuffle(self):
        random.shuffle(self.cards)

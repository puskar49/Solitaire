#    deck.py
#    Copyright (C) 2018 Mike Puskar
#
#    This program is free software: you can redistribute it and/or modify it under the terms
#    of the GNU General Public License as published by the Free Software Foundation, either
#    version 3 of the License, or any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.

from card import Card
import random


class Deck(object):
    def __init__(self):
        self.cards = []
        for pips in range(1, 14):
            for suit in ["spades", "clubs", "diamonds", "hearts"]:
                self.cards.append(Card(pips, suit))
        self.shuffle()

    @property
    def is_empty(self):
        return len(self.cards) == 0

    def deal(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None

    def shuffle(self):
        random.shuffle(self.cards)

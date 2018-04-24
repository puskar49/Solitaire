#    pile_group.py
#    Copyright (C) 2018 Mike Puskar
#
#    This program is free software: you can redistribute it and/or modify it under the terms
#    of the GNU General Public License as published by the Free Software Foundation, either
#    version 3 of the License, or any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.

import pile


class PileGroup(object):
    def __init__(self):
        self.piles = []

    def add(self, moving_pile, mouse_pos):
        moving_pile.snap_back()

    def contains_pos(self, mouse_pos):
        for item in self.piles:
            if item.contains_pos(mouse_pos):
                return True
        return False

    def draw(self, surface):
        for item in self.piles:
            item.draw(surface)

    def grab(self, mouse_pos):
        return None


class BuildingPileGroup(PileGroup):
    def __init__(self, deck):
        super().__init__()
        for index in range(7):
            self.piles.append(
                pile.BuildingPile(
                    location=(100 + (index * 150), 250),
                    deck=deck,
                    count=(index + 1)
                )
            )

    def add(self, moving_pile, mouse_pos):
        for entry in self.piles:
            if entry.contains_pos(mouse_pos):
                if entry == moving_pile.source_pile:
                    break
                elif entry.can_accept(moving_pile):
                    cards = moving_pile.pop()
                    for card in reversed(cards):
                        entry.add(card)
                    if isinstance(moving_pile.source_pile, pile.BuildingPile):
                        moving_pile.source_pile.flip()
                    return
                else:
                    break
        moving_pile.snap_back()

    def grab(self, mouse_pos):
        for entry in self.piles:
            if entry.contains_pos(mouse_pos):
                return entry.grab(mouse_pos)
        return None


class FinishedPileGroup(PileGroup):
    def __init__(self):
        super().__init__()
        for index in range(4):
            self.piles.append(
                pile.FinishedPile(
                    location=(550 + (index * 150), 50)
                )
            )

    def add(self, moving_pile, mouse_pos):
        for entry in self.piles:
            if entry.contains_pos(mouse_pos):
                if entry == moving_pile.source_pile:
                    break
                elif entry.can_accept(moving_pile):
                    cards = moving_pile.pop()
                    for card in cards:
                        entry.add(card)
                    if isinstance(moving_pile.source_pile, pile.BuildingPile):
                        moving_pile.source_pile.flip()
                    return
                else:
                    break
        moving_pile.snap_back()


class IteratingPileGroup(PileGroup):
    def __init__(self, deck):
        super().__init__()
        self.piles.append(pile.Pile(location=(100, 50)))
        while not deck.is_empty:
            self.piles[0].add(deck.deal())
        self.piles.append(pile.Pile(location=(250, 50)))

    def grab(self, mouse_pos):
        if self.piles[0].contains_pos(mouse_pos):
            if self.piles[0].size > 0:
                for card in self.piles[0].pop(3):
                    self.piles[1].add(card)
            else:
                if self.piles[1].size > 0:
                    for card in self.piles[1].pop():
                        card.flip(face_up=False)
                        self.piles[0].add(card)
            return None
        elif self.piles[1].contains_pos(mouse_pos):
            return self.piles[1].grab(mouse_pos)
        return None

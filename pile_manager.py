#    pile_manager.py
#    Copyright (C) 2018 Mike Puskar
#
#    This program is free software: you can redistribute it and/or modify it under the terms
#    of the GNU General Public License as published by the Free Software Foundation, either
#    version 3 of the License, or any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.

import deck
import pile_group
import pygame


class PileManager(object):
    def __init__(self, screen):
        self.screen = screen
        self._deck = deck.Deck()
        self._deck.shuffle()
        self.pile_groups = self._initialize_pile_groups()
        self.moving_pile = None

    def draw(self):
        for group in self.pile_groups:
            group.draw(self.screen)
        if self.moving_pile is not None:
            self.moving_pile.draw(self.screen)

    def handle(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for group in self.pile_groups:
                if group.contains_pos(mouse_pos):
                    self.moving_pile = group.grab(mouse_pos)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.moving_pile is None:
                return
            for group in self.pile_groups:
                if group.contains_pos(mouse_pos):
                    group.add(self.moving_pile, mouse_pos)
                    self.moving_pile = None
                    return
            self.moving_pile.snap_back()
            self.moving_pile = None
        elif event.type == pygame.MOUSEMOTION:
            if self.moving_pile is not None:
                self.moving_pile.snap_mouse(mouse_pos)

    def _initialize_pile_groups(self):
        pile_groups = [
            pile_group.BuildingPileGroup(self._deck),
            pile_group.FinishedPileGroup(),
            pile_group.IteratingPileGroup(self._deck)
        ]
        return pile_groups

from pathlib import Path
import pygame

OFFSET = 30

class Pile(object):
    def __init__(self, location):
        self.cards = []
        self.location = location
        self.image, self.rect = self._get_empty_image()

    def add(self, card):
        card.set_location(self.location)
        self.cards.append(card)

    def can_accept(self, moving_pile):
        return True

    def contains_pos(self, mouse_pos):
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                return True
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self, surface):
        if not self.cards:
            surface.blit(self.image, self.rect)
        else:
            for card in self.cards:
                surface.blit(card.image, card.rect)

    def grab(self, mouse_pos):
        if not self.cards:
            return None
        moving_pile = MovingPile(location=mouse_pos, source_pile=self)
        moving_pile.add(self.cards.pop(-1))
        return moving_pile

    def pop(self, count=None):
        cards = []
        if count is None:
            count = self.size()
        for index in range(min(count, self.size())):
            cards.append(self.cards.pop(-1))
            cards[-1].flip(face_up=True)
        return cards

    def size(self):
        return len(self.cards)

    def _get_empty_image(self):
        if self.location is None:
            return None, None
        image = pygame.image.load(
            str(Path("__file__").parent / "cards" / "empty.png")
        ).convert()
        base_width, base_height = image.get_size()
        new_width = int(base_width * 0.75)
        new_height = int(base_height * 0.75)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
        rect = image.get_rect()
        rect.x = self.location[0]
        rect.y = self.location[1]
        return image, rect


class BuildingPile(Pile):
    def __init__(self, location, deck, count):
        super().__init__(location)
        for dummy in range(count):
            card = deck.deal()
            card.set_location(self.location)
            self.cards.append(card)
        self.offset = 0
        self.flip()

    def add(self, card):
        location = (self.location[0], self.location[1] + self.offset)
        card.set_location(location)
        self.cards.append(card)
        self.offset += OFFSET

    def can_accept(self, moving_pile):
        if self.size() == 0:
            return moving_pile.is_king_high
        my_card = self.cards[-1]
        your_card = moving_pile.cards[0]
        if my_card.pips - your_card.pips == 1:
            if my_card.suit in ["hearts", "diamonds"]:
                return your_card.suit in ["clubs", "spades"]
            else:
                return your_card.suit in ["hearts", "diamonds"]
        return False

    def flip(self):
        if self.size() > 0:
            self.cards[-1].flip(face_up=True)
            self.offset += OFFSET

    def grab(self, mouse_pos):
        if not self.cards:
            return None
        moving_pile = MovingPile(location=mouse_pos, source_pile=self)
        for index, card in reversed(list(enumerate(self.cards))):
            if self.cards[index].rect.collidepoint(mouse_pos):
                keep_popping = True
                while keep_popping:
                    try:
                        moving_pile.add(self.cards.pop(index))
                    except IndexError:
                        keep_popping = False
                self.offset -= (OFFSET * moving_pile.size())
                return moving_pile


class FinishedPile(Pile):
    def can_accept(self, moving_pile):
        if moving_pile.size() == 1:
            if self.size() == 0:
                return moving_pile.is_ace
            else:
                my_card = self.cards[-1]
                your_card = moving_pile.cards[0]
                return my_card.suit == your_card.suit and (your_card.pips - my_card.pips) == 1
        return False


class MovingPile(Pile):
    def __init__(self, location, source_pile):
        super().__init__(location)
        self.source_pile = source_pile

    @property
    def is_ace(self):
        return len(self.cards) == 1 and self.cards[0].pips == 1

    @property
    def is_king_high(self):
        return self.cards[0].pips == 13

    def add(self, card):
        card.grab(self.location)
        self.cards.append(card)

    def draw(self, surface):
        if self.cards:
            for card in self.cards:
                surface.blit(card.image, card.rect)

    def snap_back(self):
        keep_popping = True
        while keep_popping:
            try:
                self.source_pile.add(self.cards.pop(0))
            except IndexError:
                keep_popping = False

    def snap_mouse(self, mouse_pos):
        for card in self.cards:
            card.snap_mouse(mouse_pos)

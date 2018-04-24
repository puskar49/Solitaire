#    game.py
#    Copyright (C) 2018 Mike Puskar
#
#    This program is free software: you can redistribute it and/or modify it under the terms
#    of the GNU General Public License as published by the Free Software Foundation, either
#    version 3 of the License, or any later version.
#
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.

import pygame
import pile_manager

RESOLUTION = (1280, 1024)


class Game(object):
    def __init__(self):
        self.playing = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(RESOLUTION).convert()
        self.background.fill((0, 64, 0))
        self.pile_manager = pile_manager.PileManager(self.screen)
        pygame.display.set_caption("Solitaire")
        pygame.mouse.set_visible(True)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pile_manager.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN or \
                    event.type == pygame.MOUSEBUTTONUP or \
                    event.type == pygame.MOUSEMOTION:
                self.pile_manager.handle(event)

    def run(self):
        pygame.init()
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.handle_events()
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

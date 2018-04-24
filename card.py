from pathlib import Path
import pygame

CARD_PATH = Path("__file__").parent / "cards"


class Card(pygame.sprite.Sprite):
    def __init__(self, pips, suit):
        super().__init__()
        self.pips = pips
        self.suit = suit
        self._images = self._get_images()
        self.image = self._images[0]
        self.rect = self._images[0].get_rect()
        self._face_up = 0
        self._is_grabbed = False
        self._mouse_offset = [0, 0]

    def flip(self, face_up=True):
        self._face_up = int(face_up)
        self.update_image()

    def is_face_up(self):
        return self._face_up == 1

    def snap_mouse(self, mouse_pos):
        # todo - prevent card from going off screen
        self.rect.x = mouse_pos[0] - self._mouse_offset[0]
        self.rect.y = mouse_pos[1] - self._mouse_offset[1]

    def grab(self, mouse_pos):
        self._mouse_offset = [mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y]
        self._is_grabbed = True

    def update_image(self):
        self.image = self._images[int(self._face_up)]

    def release(self):
        self._is_grabbed = False

    def set_location(self, location):
        self.rect.x = location[0]
        self.rect.y = location[1]

    def _get_images(self):
        back_file = CARD_PATH / "back.png"
        card_file = CARD_PATH / "{}_{}.png".format(self.pips, self.suit)
        images = [
            pygame.image.load(str(back_file)).convert(),
            pygame.image.load(str(card_file)).convert()
        ]
        base_width, base_height = images[0].get_size()
        new_width = int(base_width * 0.75)
        new_height = int(base_height * 0.75)
        for index, image in enumerate(images):
            images[index] = pygame.transform.smoothscale(image, (new_width, new_height))
        return images

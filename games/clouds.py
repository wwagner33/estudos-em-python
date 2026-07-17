import pygame
from pygame.sprite import Sprite

class Cloud(Sprite):
    """Representa uma única nuvem de fundo."""

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/cloud.png')
        self.rect = self.image.get_rect()

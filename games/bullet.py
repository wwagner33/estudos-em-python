import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Representa um tiro disparado pela nave."""

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Cria o retângulo do tiro em (0, 0) e o posiciona corretamente
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Posição do tiro guardada como float, para movimento suave
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move o tiro para cima na tela."""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o tiro na tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)

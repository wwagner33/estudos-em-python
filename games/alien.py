import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Representa um único alienígena da frota."""

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Não há asset de imagem para o alien no projeto; desenhamos um
        # corpo simples (elipse verde com dois "olhos") em uma Surface.
        self.image = self._build_image()
        self.rect = self.image.get_rect()

        # Cada novo alien começa perto do canto superior esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Posição horizontal exata do alien, guardada como float
        self.x = float(self.rect.x)

    @staticmethod
    def _build_image():
        """Constrói a imagem do alien sem depender de um arquivo externo."""
        width, height = 44, 32
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        body_color = (60, 180, 90)
        eye_color = (20, 20, 20)
        pygame.draw.ellipse(image, body_color, (0, 6, width, height - 6))
        pygame.draw.circle(image, eye_color, (width // 3, height // 2 + 2), 4)
        pygame.draw.circle(image, eye_color, (2 * width // 3, height // 2 + 2), 4)
        return image

    def check_edges(self):
        """Retorna True se o alien estiver na borda esquerda ou direita da tela."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Move o alien para a direita ou para a esquerda."""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

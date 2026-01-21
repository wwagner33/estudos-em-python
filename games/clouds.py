import pygame

class Clouds():
    def __init__(self, screen):
        # Insere a nuvem na tela
        self.screen = screen
        
        self.image = pygame.image.load('images/cloud.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Cria 4 cópias da nuvem em posições diferentes
        self.rect.x = self.screen_rect.width * 0.2
        self.rect.y = self.screen_rect.height * 0.1
        self.rect2 = self.image.get_rect()
        self.rect2.x = self.screen_rect.width * 0.5
        self.rect2.y = self.screen_rect.height * 0.15
        self.rect3 = self.image.get_rect()
        self.rect3.x = self.screen_rect.width * 0.7
        self.rect3.y = self.screen_rect.height * 0.05
        self.rect4 = self.image.get_rect()
        self.rect4.x = self.screen_rect.width * 0.9
        self.rect4.y = self.screen_rect.height * 0.2
            
    def blitme(self):
        # Desenha as nuvens na tela
        self.screen.blit(self.image, self.rect)
        

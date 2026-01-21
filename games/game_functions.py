import sys
import pygame

def check_events():
    """Observa eventos de teclado e mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
def update_screen(screen, ai_settings, ship, clouds):
    """Redesenha a tela e atualiza as imagens nela."""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    clouds.blitme()
    pygame.display.flip()

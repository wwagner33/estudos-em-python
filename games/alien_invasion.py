import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from game_functions import (
    check_events,
    update_bullets,
    update_aliens,
    create_fleet,
    create_clouds,
    update_screen,
)

def run_game():
    #Inicializa e cria um objeto de tela
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
     )

    pygame.display.set_caption("Invasão Alienígena")

    # Cria as estatísticas do jogo, a espaçonave e os grupos de sprites
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    create_fleet(ai_settings, screen, ship, aliens)
    create_clouds(screen, clouds)

    # Inicia o loop principal do jogo
    while True:
        check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            update_bullets(ai_settings, screen, stats, ship, aliens, bullets)
            update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        update_screen(ai_settings, screen, stats, ship, aliens, bullets, clouds)


run_game()

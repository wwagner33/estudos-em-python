import sys
import pygame

from bullet import Bullet
from alien import Alien
from clouds import Cloud


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a teclas pressionadas."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """Responde a teclas liberadas."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara um novo tiro, respeitando o limite permitido."""
    if len(bullets) < ai_settings.bullets_allowed:
        bullets.add(Bullet(ai_settings, screen, ship))


def check_events(ai_settings, screen, ship, bullets):
    """Observa eventos de teclado e mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_bullets(ai_settings, screen, stats, ship, aliens, bullets):
    """Atualiza a posição dos tiros e descarta os que saíram da tela."""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets):
    """Trata as colisões entre tiros e aliens."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)

    if len(aliens) == 0:
        # A frota inteira foi destruída: limpa os tiros e cria uma nova frota
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Calcula quantos aliens cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x // (2 * alien_width))


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calcula quantas linhas de aliens cabem na tela."""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y // (2 * alien_height))


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Cria um alien e o posiciona na linha."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Cria a frota completa de aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alien atingiu uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Desce a frota inteira e inverte sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Responde ao fato da nave ter sido atingida por um alien."""
    if stats.ships_left > 1:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        pygame.time.wait(500)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Verifica se algum alien atingiu a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Verifica se a frota está na borda e atualiza as posições dos aliens."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def create_clouds(screen, clouds):
    """Cria as nuvens de fundo em posições fixas."""
    positions = [(0.2, 0.1), (0.5, 0.15), (0.7, 0.05), (0.9, 0.2)]
    screen_rect = screen.get_rect()
    for x_frac, y_frac in positions:
        cloud = Cloud(screen)
        cloud.rect.x = screen_rect.width * x_frac
        cloud.rect.y = screen_rect.height * y_frac
        clouds.add(cloud)


def show_score(ai_settings, screen, stats):
    """Exibe a pontuação atual no canto superior direito da tela."""
    font = pygame.font.SysFont(None, 36)
    score_str = "Pontuação: {:,}".format(stats.score)
    score_image = font.render(score_str, True, ai_settings.text_color, ai_settings.bg_color)
    score_rect = score_image.get_rect()
    score_rect.right = screen.get_rect().right - 20
    score_rect.top = 20
    screen.blit(score_image, score_rect)


def show_game_over(screen):
    """Exibe a mensagem de fim de jogo no centro da tela."""
    font = pygame.font.SysFont(None, 64)
    text_image = font.render("GAME OVER", True, (200, 30, 30))
    text_rect = text_image.get_rect()
    text_rect.center = screen.get_rect().center
    screen.blit(text_image, text_rect)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, clouds):
    """Redesenha a tela e atualiza as imagens nela."""
    screen.fill(ai_settings.bg_color)
    clouds.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    show_score(ai_settings, screen, stats)

    if not stats.game_active:
        show_game_over(screen)

    pygame.display.flip()

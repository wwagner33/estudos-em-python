import pygame
import pytest

from alien import Alien
from bullet import Bullet
import game_functions as gf


def _place_alien(alien, x, y):
    """Posiciona um alien manualmente, sincronizando o atributo float `x`
    usado internamente por Alien.update() -- sem isso, a próxima chamada a
    update() sobrescreveria a posição forçada com base na posição antiga."""
    alien.rect.x = x
    alien.rect.y = y
    alien.x = float(alien.rect.x)


def _place_bullet_on(bullet, target_rect):
    bullet.rect.center = target_rect.center
    bullet.y = float(bullet.rect.y)


# --- eventos de teclado -----------------------------------------------------

def test_keydown_right_sets_moving_right(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)

    gf.check_keydown_events(event, ai_settings, screen, ship, bullets)

    assert ship.moving_right is True


def test_keyup_right_clears_moving_right(ship):
    ship.moving_right = True
    event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)

    gf.check_keyup_events(event, ship)

    assert ship.moving_right is False


def test_keydown_left_sets_moving_left(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)

    gf.check_keydown_events(event, ai_settings, screen, ship, bullets)

    assert ship.moving_left is True


def test_keyup_left_clears_moving_left(ship):
    ship.moving_left = True
    event = pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT)

    gf.check_keyup_events(event, ship)

    assert ship.moving_left is False


def test_keydown_space_fires_a_bullet(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

    gf.check_keydown_events(event, ai_settings, screen, ship, bullets)

    assert len(bullets) == 1


def test_check_events_quit_raises_systemexit(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    with pytest.raises(SystemExit):
        gf.check_events(ai_settings, screen, ship, bullets)


def test_check_events_dispatches_keydown_through_the_real_queue(ai_settings, screen, ship):
    """Ao contrário de test_keydown_right_sets_moving_right, aqui o evento passa
    pela fila real do pygame e por check_events(), cobrindo o roteamento
    KEYDOWN -> check_keydown_events (não só o handler chamado direto)."""
    bullets = pygame.sprite.Group()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

    gf.check_events(ai_settings, screen, ship, bullets)

    assert ship.moving_right is True


def test_check_events_dispatches_keyup_through_the_real_queue(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    ship.moving_right = True
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT))

    gf.check_events(ai_settings, screen, ship, bullets)

    assert ship.moving_right is False


# --- tiros -------------------------------------------------------------------

def test_fire_bullet_respects_the_allowed_limit(ai_settings, screen, ship):
    bullets = pygame.sprite.Group()
    for _ in range(ai_settings.bullets_allowed + 5):
        gf.fire_bullet(ai_settings, screen, ship, bullets)

    assert len(bullets) == ai_settings.bullets_allowed


def test_update_bullets_removes_bullets_that_left_the_screen(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    bullets = pygame.sprite.Group()
    # mantém a frota não vazia para isolar o laço de remoção de tiros do
    # respawn automático que acontece quando len(aliens) == 0
    aliens = pygame.sprite.Group()
    aliens.add(Alien(ai_settings, screen))

    bullet = Bullet(ai_settings, screen, ship)
    bullet.rect.bottom = -1
    bullet.y = float(bullet.rect.y)
    bullets.add(bullet)

    gf.update_bullets(ai_settings, screen, stats, ship, aliens, bullets)

    assert len(bullets) == 0
    assert len(aliens) == 1


# --- frota de aliens -----------------------------------------------------------

def test_create_fleet_populates_aliens_in_a_grid(ai_settings, screen, ship):
    aliens = pygame.sprite.Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    alien_width = Alien(ai_settings, screen).rect.width
    expected_columns = gf.get_number_aliens_x(ai_settings, alien_width)
    expected_rows = gf.get_number_rows(ai_settings, ship.rect.height, Alien(ai_settings, screen).rect.height)

    assert len(aliens) == expected_columns * expected_rows
    assert len(aliens) > 0


def test_check_fleet_edges_flips_direction_and_drops_fleet(ai_settings, screen):
    aliens = pygame.sprite.Group()
    alien = Alien(ai_settings, screen)
    screen_rect = screen.get_rect()
    _place_alien(alien, screen_rect.width - alien.rect.width, 100)
    aliens.add(alien)

    start_direction = ai_settings.fleet_direction
    start_y = alien.rect.y

    gf.check_fleet_edges(ai_settings, aliens)

    assert ai_settings.fleet_direction == -start_direction
    assert alien.rect.y == start_y + ai_settings.fleet_drop_speed


def test_check_fleet_edges_does_nothing_when_no_alien_at_border(ai_settings, screen):
    aliens = pygame.sprite.Group()
    alien = Alien(ai_settings, screen)
    screen_rect = screen.get_rect()
    _place_alien(alien, screen_rect.centerx, 100)
    aliens.add(alien)

    start_direction = ai_settings.fleet_direction
    start_y = alien.rect.y

    gf.check_fleet_edges(ai_settings, aliens)

    assert ai_settings.fleet_direction == start_direction
    assert alien.rect.y == start_y


# --- colisões tiro-alien -----------------------------------------------------

def test_bullet_alien_collision_removes_both_and_scores_points(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    alien = Alien(ai_settings, screen)
    aliens.add(alien)

    bullet = Bullet(ai_settings, screen, ship)
    _place_bullet_on(bullet, alien.rect)
    bullets.add(bullet)

    gf.check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)

    assert stats.score == ai_settings.alien_points
    # a frota original (1 alien) foi eliminada, então uma nova frota completa
    # é criada automaticamente e os tiros restantes são descartados
    assert len(aliens) > 1
    assert len(bullets) == 0


def test_bullet_that_misses_does_not_score_or_remove_alien(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    alien = Alien(ai_settings, screen)
    _place_alien(alien, 0, 0)
    aliens.add(alien)

    bullet = Bullet(ai_settings, screen, ship)
    screen_rect = screen.get_rect()
    bullet.rect.center = screen_rect.bottomright
    bullet.y = float(bullet.rect.y)
    bullets.add(bullet)

    gf.check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)

    assert stats.score == 0
    assert len(aliens) == 1
    assert len(bullets) == 1


# --- nave atingida / fim de jogo ---------------------------------------------

def test_ship_hit_with_lives_left_resets_fleet_and_bullets(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    assert stats.ships_left >= 2  # pré-condição do cenário: ainda restam vidas depois desta colisão

    aliens = pygame.sprite.Group()
    aliens.add(Alien(ai_settings, screen))
    bullets = pygame.sprite.Group()
    bullets.add(Bullet(ai_settings, screen, ship))

    start_lives = stats.ships_left

    gf.ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    assert stats.ships_left == start_lives - 1
    assert stats.game_active is True
    assert len(bullets) == 0
    assert len(aliens) > 0  # uma nova frota foi criada
    screen_rect = screen.get_rect()
    assert ship.rect.centerx == screen_rect.centerx


def test_ship_hit_on_last_life_ends_the_game(ai_settings, screen, ship):
    from game_stats import GameStats

    ai_settings.ship_limit = 1
    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    gf.ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    assert stats.game_active is False
    assert stats.ships_left == 1


def test_check_aliens_bottom_triggers_ship_hit(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    alien = Alien(ai_settings, screen)
    screen_rect = screen.get_rect()
    _place_alien(alien, 100, screen_rect.bottom)
    aliens.add(alien)

    start_lives = stats.ships_left

    gf.check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

    assert stats.ships_left == start_lives - 1


def test_update_aliens_ship_collision_triggers_ship_hit(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    alien = Alien(ai_settings, screen)
    _place_alien(alien, ship.rect.x, ship.rect.y)
    aliens.add(alien)

    start_lives = stats.ships_left

    gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

    assert stats.ships_left == start_lives - 1


# --- renderização (smoke tests) ----------------------------------------------

def test_update_screen_does_not_raise_while_active(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, clouds)


def test_update_screen_does_not_raise_on_game_over(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    stats.game_active = False
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, clouds)


def test_update_screen_draws_pending_bullets(ai_settings, screen, ship):
    from game_stats import GameStats

    stats = GameStats(ai_settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bullets.add(Bullet(ai_settings, screen, ship))
    clouds = pygame.sprite.Group()

    gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, clouds)

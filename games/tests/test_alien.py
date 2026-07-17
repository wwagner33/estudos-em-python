from alien import Alien


def test_alien_starts_near_top_left_corner(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    assert alien.rect.x == alien.rect.width
    assert alien.rect.y == alien.rect.height


def test_check_edges_true_at_right_border(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    screen_rect = screen.get_rect()
    alien.rect.right = screen_rect.right
    assert alien.check_edges() is True


def test_check_edges_true_at_left_border(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    alien.rect.left = 0
    assert alien.check_edges() is True


def test_check_edges_false_in_the_middle(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    screen_rect = screen.get_rect()
    alien.rect.centerx = screen_rect.centerx
    assert alien.check_edges() is False


def test_update_moves_alien_according_to_fleet_direction(ai_settings, screen):
    ai_settings.fleet_direction = 1
    alien = Alien(ai_settings, screen)
    start_x = alien.rect.x

    alien.update()

    assert alien.rect.x == start_x + ai_settings.alien_speed_factor


def test_update_moves_alien_left_when_fleet_direction_is_reversed(ai_settings, screen):
    ai_settings.fleet_direction = -1
    alien = Alien(ai_settings, screen)
    start_x = alien.rect.x

    alien.update()

    assert alien.rect.x == start_x - ai_settings.alien_speed_factor

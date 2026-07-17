from ship import Ship


def test_ship_starts_centered_at_screen_bottom(ai_settings, screen):
    ship = Ship(ai_settings, screen)
    screen_rect = screen.get_rect()
    assert ship.rect.centerx == screen_rect.centerx
    assert ship.rect.bottom == screen_rect.bottom


def test_moving_right_increases_centerx(ship):
    start_centerx = ship.rect.centerx
    ship.moving_right = True
    ship.update()
    assert ship.rect.centerx > start_centerx


def test_moving_left_decreases_centerx(ship):
    start_centerx = ship.rect.centerx
    ship.moving_left = True
    ship.update()
    assert ship.rect.centerx < start_centerx


def test_ship_does_not_move_past_right_edge(ship, screen):
    screen_rect = screen.get_rect()
    ship.moving_right = True
    for _ in range(3000):
        ship.update()
    assert ship.rect.right <= screen_rect.right


def test_ship_does_not_move_past_left_edge(ship):
    ship.moving_left = True
    for _ in range(3000):
        ship.update()
    assert ship.rect.left >= 0


def test_center_ship_recenters_after_moving(ship, screen):
    ship.moving_left = True
    for _ in range(50):
        ship.update()

    ship.center_ship()

    screen_rect = screen.get_rect()
    assert ship.rect.centerx == screen_rect.centerx

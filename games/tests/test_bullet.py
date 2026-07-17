from bullet import Bullet


def test_bullet_spawns_at_ship_top_center(ai_settings, screen, ship):
    bullet = Bullet(ai_settings, screen, ship)
    assert bullet.rect.centerx == ship.rect.centerx
    assert bullet.rect.top == ship.rect.top


def test_bullet_moves_up_on_update(ai_settings, screen, ship):
    bullet = Bullet(ai_settings, screen, ship)
    start_y = bullet.rect.y

    bullet.update()

    assert bullet.rect.y == start_y - ai_settings.bullet_speed_factor


def test_draw_bullet_does_not_raise(ai_settings, screen, ship):
    bullet = Bullet(ai_settings, screen, ship)
    bullet.draw_bullet()

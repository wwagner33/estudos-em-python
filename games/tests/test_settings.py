from settings import Settings


def test_default_screen_settings():
    ai_settings = Settings()
    assert ai_settings.screen_width == 1200
    assert ai_settings.screen_height == 800


def test_default_gameplay_settings_are_positive():
    ai_settings = Settings()
    assert ai_settings.ship_speed_factor > 0
    assert ai_settings.ship_limit > 0
    assert ai_settings.bullet_speed_factor > 0
    assert ai_settings.bullets_allowed > 0
    assert ai_settings.alien_speed_factor > 0
    assert ai_settings.fleet_drop_speed > 0
    assert ai_settings.alien_points > 0


def test_fleet_direction_starts_moving_right():
    ai_settings = Settings()
    assert ai_settings.fleet_direction == 1

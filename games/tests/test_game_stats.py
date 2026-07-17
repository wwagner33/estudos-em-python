from game_stats import GameStats


def test_new_game_starts_active_with_full_lives_and_zero_score(ai_settings):
    stats = GameStats(ai_settings)
    assert stats.game_active is True
    assert stats.ships_left == ai_settings.ship_limit
    assert stats.score == 0


def test_reset_stats_restores_initial_values(ai_settings):
    stats = GameStats(ai_settings)
    stats.score = 500
    stats.ships_left = 0

    stats.reset_stats()

    assert stats.score == 0
    assert stats.ships_left == ai_settings.ship_limit

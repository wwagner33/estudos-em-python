class GameStats():
    """Acompanha as estatísticas do jogo."""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # O jogo começa ativo
        self.game_active = True

    def reset_stats(self):
        """Inicializa estatísticas que podem mudar durante o jogo."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

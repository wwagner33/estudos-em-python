class Settings():
    def __init__(self):
        # Configurações da tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (51, 153, 255)

        # Configurações da nave
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Configurações dos tiros
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Configurações dos aliens
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction = 1 representa direita; -1 representa esquerda
        self.fleet_direction = 1
        self.alien_points = 50

        # Cor do texto de pontuação
        self.text_color = (30, 30, 30)

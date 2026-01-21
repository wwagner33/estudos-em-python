import sys
import pygame
from settings import Settings
from ship import Ship
from game_functions import check_events, update_screen
from clouds import Clouds

def run_game():
    #Inicializa e cria um objeto de tela
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
     )
   
    pygame.display.set_caption("Invasão Alienígena")
    
    # Cria uma espaçonave
    ship = Ship(screen)
    clouds = Clouds(screen)
    
    # Inicia o loop principal do jogo
    while True:
        check_events()
        update_screen(screen, ai_settings, ship, clouds)
        

run_game()
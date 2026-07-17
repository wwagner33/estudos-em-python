import os
import sys

# pygame precisa de um driver de vídeo mesmo sem display real; "dummy"
# permite pygame.init()/set_mode() em ambiente headless (CI, terminal sem X).
os.environ["SDL_VIDEODRIVER"] = "dummy"

GAMES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GAMES_DIR not in sys.path:
    sys.path.insert(0, GAMES_DIR)

import pygame  # noqa: E402
import pytest  # noqa: E402

from settings import Settings  # noqa: E402
from game_stats import GameStats  # noqa: E402
from ship import Ship  # noqa: E402


@pytest.fixture(autouse=True, scope="session")
def _chdir_to_games():
    """As imagens são carregadas com caminhos relativos (ex.: 'images/ship-human.png'),
    então os testes precisam rodar com cwd em games/, não importa de onde o pytest foi chamado."""
    previous_cwd = os.getcwd()
    os.chdir(GAMES_DIR)
    yield
    os.chdir(previous_cwd)


@pytest.fixture(autouse=True, scope="session")
def _pygame_session(_chdir_to_games):
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def ai_settings():
    return Settings()


@pytest.fixture
def screen(ai_settings):
    return pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))


@pytest.fixture
def stats(ai_settings):
    return GameStats(ai_settings)


@pytest.fixture
def ship(ai_settings, screen):
    return Ship(ai_settings, screen)

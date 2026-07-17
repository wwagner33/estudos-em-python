import pygame

from clouds import Cloud
from game_functions import create_clouds


def test_cloud_is_a_sprite_with_image_and_rect(screen):
    cloud = Cloud(screen)
    assert isinstance(cloud, pygame.sprite.Sprite)
    assert cloud.image is not None
    assert cloud.rect is not None


def test_create_clouds_adds_four_clouds_to_the_group(screen):
    clouds = pygame.sprite.Group()
    create_clouds(screen, clouds)
    assert len(clouds) == 4


def test_create_clouds_positions_are_within_screen_bounds(screen):
    clouds = pygame.sprite.Group()
    create_clouds(screen, clouds)
    screen_rect = screen.get_rect()

    for cloud in clouds.sprites():
        assert screen_rect.left <= cloud.rect.x <= screen_rect.right
        assert screen_rect.top <= cloud.rect.y <= screen_rect.bottom

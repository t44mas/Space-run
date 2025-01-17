# Глобальные переменные
import pygame

SHIP_SPEED = 7
SHIP_HEALTH = 3
BULLET_SPEED = 8
ENEMY_SPEED = 5
BIG_ENEMY_SPEED = 1
FPS = 40
MUSIC_VOLUME = 0.1
EFFECT_VOLUME = 0.1
ROCKET_SPEED = 2
# получаем информацию о дисплее
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w - 100
screen_height = info.current_h - 100
size = screen_width, screen_height

# Глобальные переменные
import pygame

SHIP_SPEED = 6
SHIP_HEALTH = 3
BULLET_SPEED = 8
ENEMY_SPEED = 5
BIG_ENEMY_SPEED = 1
FPS = 40
MUSIC_VOLUME = 0.1
EFFECT_VOLUME = 0.1
ROCKET_SPEED = 4
# получаем информацию о дисплее
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
size = screen_width, screen_height
#дб
db_file = 'records.db'
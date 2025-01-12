from classes import MainShip, Bullet, EnemyShip, HP, HPBoost, SHIP_SPEED
from classes import all_sprites, enemy_sprites, bullets_sprites, boosts_sprites, start_screen
from config import size, screen_width, screen_height, FPS, MUSIC_VOLUME, EFFECT_VOLUME
from levels import level_one
import pygame

# Переменные
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 40)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


screen_state = start_screen(screen, clock, FPS, screen_width, screen_height)

# Обработка 'кнопок'
if screen_state == "game":
    level_one(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites, bullets_sprites, boosts_sprites, my_font)


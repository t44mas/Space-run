from classes import MainShip, Bullet, EnemyShip, HP, HPBoost, SHIP_SPEED
from classes import all_sprites, enemy_sprites, boosts_sprites, enemy_bullets_sprites, \
    player_bullets_sprites
from config import size, screen_width, screen_height, FPS, MUSIC_VOLUME, EFFECT_VOLUME
from levels import level_one, start_screen, lose_screen
import pygame

# Переменные
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 40)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

screen_state = start_screen(screen, clock, FPS, screen_width, screen_height)
# Обработка 'кнопок'
while True:
    if screen_state == "game":
        screen_state = level_one(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites,
                             boosts_sprites, my_font)
    if screen_state == "lose":
        screen_state = lose_screen(screen, clock, FPS, screen_width, screen_height)
    if screen_state == "exit":
        break

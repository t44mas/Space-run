from classes import MainShip, Bullet, EnemyShip, HP, HPBoost, SHIP_SPEED
from classes import all_sprites, enemy_sprites, boosts_sprites, enemy_bullets_sprites, \
    player_bullets_sprites, boss_sprite
from config import size, screen_width, screen_height, FPS, MUSIC_VOLUME, EFFECT_VOLUME, db_file
from levels import level_one, start_screen, lose_screen, get_top_scores, boss_level, win_screen
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
                             boosts_sprites,my_font)
    if screen_state == "boss":
        screen_state = boss_level(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites,
                                  boosts_sprites, boss_sprite, my_font)
    if screen_state == "win":
        screen_state = win_screen(screen, clock, FPS, screen_width, screen_height)
    if screen_state == "lose":
        screen_state = lose_screen(screen, clock, FPS, screen_width, screen_height)
    if screen_state == 'records':
        screen_state = get_top_scores(screen, clock, FPS, db_file, screen_width, screen_height)
    if screen_state == "menu":
        screen_state = start_screen(screen, clock, FPS, screen_width, screen_height)
    if screen_state == "exit":
        break

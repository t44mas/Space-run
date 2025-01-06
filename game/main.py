import os
import random
import sys
from classes import MainShip
import pygame

pygame.init()

# получаем информацию о дисплее
info = pygame.display.Info()
screen_width = info.current_w - 100
screen_height = info.current_h - 100
size = screen_width, screen_height

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
running = True

MainShip(screen_width, screen_height, all_sprites)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(event)

    screen.fill('black')
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(40)

pygame.quit()
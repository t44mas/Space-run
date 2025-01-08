# classes.py
import os
import sys
import random
import pygame

SHIP_SPEED = 5
BULLET_SPEED = 8
ENEMY_SPEED = 5


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class MainShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_image = load_image("MainShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 12, self.screen_height // 12))
        self.image = scaled_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height
        self.speed = SHIP_SPEED
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def update(self):
        if self.move_up:
            self.rect.y -= self.speed
        if self.move_down:
            self.rect.y += self.speed
        if self.move_left:
            self.rect.x -= self.speed
        if self.move_right:
            self.rect.x += self.speed

    # метод для движения при нажатии на клавиши wasd
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move_up = True
            if event.key == pygame.K_s:
                self.move_down = True
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_d:
                self.move_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.move_up = False
            if event.key == pygame.K_s:
                self.move_down = False
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, screen_width, screen_height, bullets, *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = x
        self.y = y
        self.direction_x = dir_x  # направление 1 (налево) или -1 (направо)
        self.bullets = bullets  # группа пуль
        original_image = load_image("EnemyShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 12, self.screen_height // 12))
        rotated_image = pygame.transform.rotate(scaled_image, +180)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.bottom = self.y
        self.speed = ENEMY_SPEED

    def update(self):
        if pygame.sprite.spritecollideany(self, self.bullets):  # проверка если попали пулей
            self.kill()



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, screen_height,  *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_image = load_image("Bullet.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 35, self.screen_height // 25))
        rotated_image = pygame.transform.rotate(scaled_image, +90)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

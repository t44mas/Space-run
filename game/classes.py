import os
import sys
import pygame
import random
from config import SHIP_SPEED, SHIP_HEALTH, BULLET_SPEED, ENEMY_SPEED
from config import screen_width, screen_height

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
boosts_sprites = pygame.sprite.Group()


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
    def __init__(self, *group):
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
        self.hp = SHIP_HEALTH
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def update(self):
        if self.move_up and self.rect.y > 0:
            self.rect.y -= self.speed
        if self.move_down and self.rect.y < self.screen_height - 100:
            self.rect.y += self.speed
        if self.move_left and self.rect.centerx > 50:
            self.rect.x -= self.speed
        if self.move_right and self.rect.centerx < self.screen_width - 50:
            self.rect.x += self.speed
        # проверка попадания пули
        if pygame.sprite.spritecollideany(self, bullets_sprites):
            b = pygame.sprite.spritecollideany(self, bullets_sprites)  # помещаем спрайт пули в переменную
            if b.enemy:  # проверка что пуля врага чтобы не получать урон от своих же пуль
                self.hp -= 1
                b.kill()
        if pygame.sprite.spritecollideany(self, boosts_sprites):
            b = pygame.sprite.spritecollideany(self, boosts_sprites)
            b.kill()
            self.hp += 1

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

    def main_ship_shooting(self):
        bullet = Bullet(self.rect.centerx, self.rect.top - 20, all_sprites,
                        bullets_sprites)


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction_x = dir_x  # направление 1(налево) или -1 (направо)
        original_image = load_image("EnemyShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 12, self.screen_height // 12))
        rotated_image = pygame.transform.rotate(scaled_image, +180)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = ENEMY_SPEED

    def update(self):
        if pygame.sprite.spritecollideany(self, bullets_sprites):  # проверка если попали пулей
            self.kill()
        if self.direction_x == 1:
            if self.rect.centerx < self.screen_width - 50:
                self.rect.centerx += self.speed
        if self.direction_x == -1:
            if self.rect.centerx > 50:
                self.rect.centerx -= self.speed
        if self.rect.centerx <= 50 or self.rect.centerx >= self.screen_width - 50:
            self.direction_x *= -1

    def enemy_shooting(self):
        bul = Bullet(self.rect.centerx, self.rect.bottom + 70,
                     bullets_sprites, all_sprites, enemy=True)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, *group, enemy=False):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_image = load_image("Bullet.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 35, self.screen_height // 25))
        if enemy:  # если пулю выпустил врат то она перевернута
            rotated_image = pygame.transform.rotate(scaled_image, +270)
        else:
            rotated_image = pygame.transform.rotate(scaled_image, +90)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
        self.enemy = enemy

    def update(self):
        if not self.enemy:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > self.screen_height:
            self.kill()


class HP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        original_image = load_image("heart2.png")
        self.image = pygame.transform.scale(original_image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y


class HPBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(boosts_sprites)
        original_image = load_image("HP_Boost.png")
        self.image = original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(64, screen_width)

    def update(self):
        self.rect.y += 5


# начальный экран
def start_screen(screen, clock, FPS, WIDTH, HEIGHT):
    intro_text = ["ЗАСТАВКА", "",
                  "Начать",
                  "рекорды",
                  "правила"]
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    # ШРИФТ
    font = pygame.font.Font(None, 30)


    text_coord = 200
    text_rects = []

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 100
        screen.blit(string_rendered, intro_rect)
        text_rects.append(intro_rect)
        text_coord += 30


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        if intro_text[i] == "Начать":
                            return "game"
                        elif intro_text[i] == "рекорды":
                            pass
                        elif intro_text[i] == "правила":
                            pass

        pygame.display.flip()
        clock.tick(FPS)



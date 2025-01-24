import os
import sys
import pygame
import random
import math
from config import SHIP_SPEED, SHIP_HEALTH, BULLET_SPEED, ENEMY_SPEED, BIG_ENEMY_SPEED, ROCKET_SPEED
from config import screen_width, screen_height
# Звуки
boom_sound = pygame.mixer.Sound('data\\Sounds\\Boom1.wav')
boom_sound.set_volume(0.2)
# Группы спрайтов
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
boosts_sprites = pygame.sprite.Group()
bullets_sprites = pygame.sprite.Group()
player_bullets_sprites = pygame.sprite.Group()
enemy_bullets_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((40, 0))
        image.set_colorkey(colorkey)
    return image


class MainShip(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_image = load_image("MainShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 18, self.screen_height // 18))
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
        if pygame.sprite.spritecollideany(self, enemy_bullets_sprites):
            b = pygame.sprite.spritecollideany(self, enemy_bullets_sprites)  # помещаем спрайт пули в переменную
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
                        player_bullets_sprites)


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, attack_speed, *group, change_dir=False):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction_x = dir_x  # направление 1(налево) или -1 (направо)
        original_image = load_image("EnemyShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 18, self.screen_height // 18))
        rotated_image = pygame.transform.rotate(scaled_image, +180)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.attack_speed = attack_speed
        self.attack_count = 1
        self.speed = ENEMY_SPEED
        self.change_dir = change_dir

    def update(self):
        collided_bullet = pygame.sprite.spritecollideany(self, player_bullets_sprites)
        if collided_bullet:  # проверка если попали пулей
            collided_bullet.kill()
            boom1 = Boom(self.image, self.rect, all_sprites, size=1.25)
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
        # кароче count как счетчик, а attack_speed чем больше, тем медленее корабль стреляет. Тоесть при attack_speed = 1 мы стреляем каждое событие выстрела, а при 2-ух каждое второе
        if self.attack_count == self.attack_speed:
            bul = Bullet(self.rect.centerx, self.rect.bottom + self.screen_width // 35,
                         enemy_bullets_sprites, all_sprites, enemy=True)
            self.attack_count = 1
        else:
            self.attack_count += 1


class BigEnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, attack_speed, *group, change_dir=False):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction_x = dir_x  # направление 1(налево) или -1 (направо)
        self.direction_y = True
        self.hp = 3
        original_image = load_image("BigEnemyShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (self.screen_width // 10, self.screen_height // 10))
        rotated_image = pygame.transform.rotate(scaled_image, +180)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.attack_speed = attack_speed
        self.attack_count = 1
        self.speed = BIG_ENEMY_SPEED
        self.change_dir = change_dir

    def update(self):
        if self.hp == 0:
            boom2 = Boom(self.image, self.rect, all_sprites, size=2)
            self.kill()
        collided_bullet = pygame.sprite.spritecollideany(self, player_bullets_sprites)
        if collided_bullet:  # проверка если попали пулей
            self.hp -= 1
            collided_bullet.kill()
        rand_speed = random.random()
        if self.direction_y:
            self.rect.bottom += self.speed
        if rand_speed < 0.3:
            if self.direction_x == 1:
                if self.rect.centerx < self.screen_width - 50:
                    self.rect.centerx += self.speed * 3
            if self.direction_x == -1:
                if self.rect.centerx > 50:
                    self.rect.centerx -= self.speed * 3
            if self.rect.centerx <= 50 or self.rect.centerx >= self.screen_width - 50:
                self.direction_x *= -1
            rand_speed = random.random()
            if rand_speed < 0.1:
                self.direction_x = -self.direction_x

    def enemy_shooting(self):
        # кароче count как счетчик, а attack_speed чем больше, тем медленее корабль стреляет. Тоесть при attack_speed = 1 мы стреляем каждое событие выстрела, а при 2-ух каждое второе
        if self.attack_count == self.attack_speed:
            bul = Bullet(self.rect.centerx, self.rect.bottom + self.screen_width // 30,
                         enemy_bullets_sprites, all_sprites, enemy=True, size=(25, 15))
            self.attack_count = 1
        else:
            self.attack_count += 1


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, player, *group):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        image = load_image("Rocket.jpg", -1)  # Загружаем изображение
        scaled_image = pygame.transform.scale(image,
                                              (self.screen_width // 15, self.screen_height // 15))
        self.original_image = pygame.transform.rotate(scaled_image,
                                                      0).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.boom_frames = []  # кадры взрыва
        self.boom_rect = None
        self.cut_sheet(load_image('boom.png', -1), 5, 5)
        self.cur_boom_frame = 0
        self.is_booming = False  # флаг для взрыва

        self.speed = ROCKET_SPEED
        self.player = player
        self.angle = 0  # угол для разворота изображения

        self.frame_delay = 2  # Задержка между кадрами
        self.frame_counter = 0  # Счетчик задержки

        self.active = True

    def update(self):
        if not self.active:
            return
        if self.is_booming:
            self.boom()
            return

        collided_bullet = pygame.sprite.spritecollideany(self, player_bullets_sprites)  # Проверка столкновения с пулей
        collided_player = pygame.sprite.spritecollideany(self, player_sprite)  # Проверка столкновения с игроком
        if collided_bullet or collided_player:
            if collided_bullet:
                boom_sound.play()
                collided_bullet.kill()
            self.is_booming = True  # запускаем флаг для анимации взрыва
            self.image = self.boom_frames[0]  # отрисовываем 1 кадр
            self.rect = self.image.get_rect(center=self.rect.center)
            if collided_player:
                collided_player.hp -= 1
            return
        # расчет направления
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # расчет длины вектора
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            normalized_x = dx / distance
            normalized_y = dy / distance
            # угол в радианах
            angle_radians = math.atan2(dy, dx)
            # градусы
            self.angle = math.degrees(angle_radians)
            # поворот в сторону игрока
            self.image = pygame.transform.rotate(self.original_image, -self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)  # Обновление прямоугольника
            # движения игрока в его сторону
            self.rect.x += normalized_x * self.speed
            self.rect.y += normalized_y * self.speed

    def cut_sheet(self, sheet, columns, rows):
        self.boom_rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                     sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.boom_rect.w * i, self.boom_rect.h * j)
                self.boom_frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.boom_rect.size)))

    def boom(self):
        # Анимация взрыва
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.cur_boom_frame += 1
            self.frame_counter = 0
            if self.cur_boom_frame < len(self.boom_frames):
                self.image = self.boom_frames[self.cur_boom_frame]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__(all_sprites)
        original_image = load_image("laser.png")
        self.image = pygame.transform.scale(original_image, (screen_width, screen_height // 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.y = y
        self.cd = 600
        self.last = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        collided_player = pygame.sprite.spritecollideany(self, player_sprite)
        if collided_player and now - self.last >= self.cd:
            self.last = now
            collided_player.hp -= 1


class Alarm(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__(all_sprites)
        original_image = load_image("alarm.png")
        self.image = pygame.transform.scale(original_image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = 64
        self.rect.y = y


class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, dir_x, attack_speed, *group, change_dir=True):
        super().__init__(*group)
        self.direction_x = dir_x  # направление 1(налево) или -1 (направо)
        original_image = load_image("smallShip.png", -1)
        scaled_image = pygame.transform.scale(original_image, (screen_width // 36, screen_height // 28))
        rotated_image = pygame.transform.rotate(scaled_image, +180)
        self.image = rotated_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.change_dir = change_dir
        self.attack_speed = attack_speed
        self.attack_count = 1
        self.speed = ENEMY_SPEED * 2

    def update(self):
        collided_bullet = pygame.sprite.spritecollideany(self, player_bullets_sprites)
        if collided_bullet:  # проверка если попали пулей
            collided_bullet.kill()
            boom3 = Boom(self.image, self.rect, all_sprites, size=1)
            self.kill()
        if self.direction_x == 1:
            if self.rect.centerx < screen_width - 50:
                self.rect.centerx += self.speed
        if self.direction_x == -1:
            if self.rect.centerx > 50:
                self.rect.centerx -= self.speed
        if self.rect.centerx <= 50 or self.rect.centerx >= screen_width - 50:
            self.direction_x *= -1

    def enemy_shooting(self):
        # кароче count как счетчик, а attack_speed чем больше, тем медленее корабль стреляет. Тоесть при attack_speed = 1 мы стреляем каждое событие выстрела, а при 2-ух каждое второе
        if self.attack_count == self.attack_speed:  # если скорость аттаки 1 то стреляем сразу
            bul = Bullet(self.rect.centerx, self.rect.bottom + screen_width // 35,
                         enemy_bullets_sprites, all_sprites, enemy=True)
            self.attack_count = 1
        else:
            self.attack_count += 1

    def changeDir(self):
        a = random.randint(0, 4)
        if a == 1:
            self.direction_x *= -1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, *group, enemy=False, size=(42, 30)):
        super().__init__(*group)
        self.screen_width = screen_width
        self.screen_height = screen_height
        original_image = load_image("Bullet.png", -1)
        scaled_image = pygame.transform.scale(original_image,
                                              (self.screen_width // size[0], self.screen_height // size[1]))
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


class Boom(pygame.sprite.Sprite):
    def __init__(self, start_image, start_rect, *group, size=1):
        super().__init__(*group)
        self.image = start_image
        self.rect = start_rect
        self.boom_frames = []  # кадры взрыва
        self.boom_rect = None
        self.cut_sheet(load_image('EnemyExplosion.png', -1), 6, 1)
        self.cur_boom_frame = 0
        self.frame_delay = 2  # Задержка между кадрами
        self.frame_counter = 0  # Счетчик задержки
        self.boom_size = size
        boom_sound.play()

    def update(self):
        self.boom()

    def cut_sheet(self, sheet, columns, rows):
        self.boom_rect = pygame.Rect(self.rect.centerx, self.rect.y, sheet.get_width() // columns,
                                     sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.boom_rect.w * i, self.boom_rect.h * j)
                self.boom_frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.boom_rect.size)))

    def boom(self):
        # Анимация взрыва
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.cur_boom_frame += 1
            self.frame_counter = 0
            if self.cur_boom_frame < len(self.boom_frames):
                scaled_image = pygame.transform.scale(self.boom_frames[self.cur_boom_frame],
                                                      (128 * self.boom_size, 128 * self.boom_size))
                self.image = scaled_image
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()


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

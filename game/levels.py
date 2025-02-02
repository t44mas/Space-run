import pygame
import random
from classes import MainShip, EnemyShip, Bullet, HPBoost, HP, BigEnemyShip, Rocket, player_sprite, Laser, Alarm, \
    SmallEnemy, load_image, Points, records, SpeedBoost, score, Boss, boss_sprite
from config import MUSIC_VOLUME, EFFECT_VOLUME
import sqlite3
# Глоб переменные
SHIP_SPEED = 5
SHOOTCD = pygame.USEREVENT + 1
ENEMYSHOOTING = pygame.USEREVENT + 2
HPBOOSTSPAWN = pygame.USEREVENT + 3
SPEEDUP = pygame.USEREVENT + 4
SPEEDUPCD = pygame.USEREVENT + 5
ALARM = pygame.USEREVENT + 6
LASERSPAWN = pygame.USEREVENT + 7
LASERDELETE = pygame.USEREVENT + 8
CHANGEENEMYDIR = pygame.USEREVENT + 9  # событие смены направления мальнького кораблся
DIEANIM = pygame.USEREVENT + 10

# Музыка и звуки
pygame.mixer.music.load('data\\Sounds\\BackSound.ogg')
sound_shoot = pygame.mixer.Sound('data\\Sounds\\Shoot.wav')
alarm_sound = pygame.mixer.Sound('data\\Sounds\\alarm1.wav')
laser_sound = pygame.mixer.Sound('data\\Sounds\\laser.wav')
sound_shoot.set_volume(EFFECT_VOLUME)
alarm_sound.set_volume(EFFECT_VOLUME / 3)
laser_sound.set_volume(0.5)
pygame.mixer.music.set_volume(MUSIC_VOLUME)  # Громкость музыки
pygame.mixer.music.play(-1)

# консты для текста и фона records
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 45)

# начальный экран
def start_screen(screen, clock, FPS, WIDTH, HEIGHT):
    intro_text = ["ЗАСТАВКА", "",
                  "Начать",
                  "рекорды"]
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
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        if intro_text[i] == "Начать":
                            return "game"
                        elif intro_text[i] == "рекорды":
                            return 'records'
                        elif intro_text[i] == "правила":
                            pass

        pygame.display.flip()
        clock.tick(FPS)


def get_top_scores(screen, clock, FPS, db_path, WIDTH, HEIGHT, limit=10):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT id, EnemyShip, BigEnemyShip, Rocket, SmallEnemy, Points
                    FROM records
                    ORDER BY id DESC
                    LIMIT ?
                """, (limit,))
        records = cursor.fetchall()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'exit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'menu'

            screen.fill(BLACK)

            title_text = font_medium.render("Последние Рекорды", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
            screen.blit(title_text, title_rect)

            y_offset = 100
            for number, (id, EnemyShip, BigEnemyShip, Rocket, SmallEnemy, Points) in enumerate(records, 1):
                text = f"{number}. id: {id},  Enemy: {EnemyShip},  BigEnemy: {BigEnemyShip},  Rocket: {Rocket},  SmallEnemy: {SmallEnemy},  Points: {Points}"
                draw_text(text, font_small, WHITE, screen, 50, y_offset)
                y_offset += 50

            draw_text("Нажмите ESC, чтобы вернуться", font_small, GRAY, screen, 50, HEIGHT - 50)

            pygame.display.flip()
            clock.tick(FPS)
    except Exception as e:
        print(f"Ошибка при работе с БД: {e}")
        return "menu"
    finally:
        if conn:
            conn.close()


def draw_text(text, font, color, surface, x, y): # рисуем текст
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.left = x
    text_rect.top = y
    surface.blit(text_obj, text_rect)

def lose_screen(screen, clock, FPS, WIDTH, HEIGHT):
    records(score.enemy, score.bigE, score.rockets, score.smallE, score.score)

    intro_text = [f"SCORE: {score.score}",
                  "",
                  "RETRY!",
                  "",
                  "Records"]
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('LoseBackground.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    # ШРИФТ
    font = pygame.font.Font(None, 40)

    text_coord = HEIGHT // 1.5
    text_rects = []

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - 50
        screen.blit(string_rendered, intro_rect)
        text_rects.append(intro_rect)
        text_coord += 30

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(text_rects):
                    if rect.collidepoint(mouse_pos):
                        if intro_text[i] == "RETRY!":
                            score.clear()
                            return "game"
                        elif intro_text[i] == "Records":
                            return 'records'

        pygame.display.flip()
        clock.tick(FPS)


# Первый левел(он не такой должен быть это к примеру)

def level_one(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites, boosts_sprites, my_font):
    running = True
    shooting = False
    can_shoot = True
    speed_boost = False

    pygame.time.set_timer(ENEMYSHOOTING, 750)
    pygame.time.set_timer(CHANGEENEMYDIR, 500)
    pygame.time.set_timer(HPBOOSTSPAWN, 15000)
    pygame.time.set_timer(SPEEDUP, 0)
    pygame.time.set_timer(SPEEDUPCD, 0)
    alarm_time = random.randint(10000, 20000)  # спавнит предупреждение о лазере от 10 до 20 сек
    pygame.time.set_timer(ALARM, alarm_time)
    pygame.time.set_timer(LASERSPAWN, alarm_time + 2000)
    pygame.time.set_timer(LASERDELETE, alarm_time + 6000)
    laser_time_change = False
    # Интерфейс
    HP1 = HP(128, 16)
    POINTS = Points(272, 16)
    SPEEDBOOST = SpeedBoost(96, 96)

    # Волны врагов
    wave1 = False
    wave2 = True
    wave3 = False
    wave4 = False

    player = MainShip(all_sprites, player_sprite)
    boss = Boss(screen_width // 2, 200, 2, player,boss_sprite)
    enemy0 = EnemyShip(50, 300, 1, 2, player, enemy_sprites)
    enemy1 = EnemyShip(300, 200, -1, 2, player,
                       enemy_sprites)  # x, y, x_dir, attack_speed(чем больше тем медленее), spriteGroup
    enemy2 = EnemyShip(600, 300, -1, 2, player, enemy_sprites)  # также есть скрытый параметр change_dir=False
    enemy3 = EnemyShip(900, 200, 1, 2, player, enemy_sprites)
    enemy4 = EnemyShip(1200, 300, -1, 2, player, enemy_sprites)
    enemy5 = EnemyShip(1500, 200, -1, 2, player, enemy_sprites)
    enemy6 = EnemyShip(1800, 300, 1, 2, player, enemy_sprites)
    # enemy3 = BigEnemyShip(300, 200, 1, 4, player, enemy_sprites)
    # rocket = Rocket(100, 100, player, all_sprites)
    # small1 = SmallEnemy(200, 200, 1, 1,player, enemy_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            player.handle_input(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shooting = True
                if event.key == pygame.K_LSHIFT:
                    if not speed_boost:  # проверяем прошло ли кд
                        SPEEDBOOST.kill()
                        player.speed += 5  # увеличиваем скорость и запускаем таймера
                        pygame.time.set_timer(SPEEDUP, 3000)
                        pygame.time.set_timer(SPEEDUPCD, 6000)
                        speed_boost = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shooting = False
            # Выстрел
            if event.type == SHOOTCD:
                can_shoot = True

            if player.hp <= 0:
                for x in all_sprites, enemy_sprites, boosts_sprites:
                    for y in x:
                        y.kill()
                return "lose"

            if shooting and can_shoot:
                player.main_ship_shooting()
                sound_shoot.play()
                pygame.time.set_timer(SHOOTCD, 500)  # запуск кд на выстрел
                can_shoot = False
            # События
            if event.type == ENEMYSHOOTING:
                for enemy in enemy_sprites:
                    enemy.enemy_shooting()
            if event.type == CHANGEENEMYDIR:  # меняет направление
                for enemy in enemy_sprites:
                    if enemy.change_dir:
                        enemy.changeDir()
            if event.type == HPBOOSTSPAWN:
                hp_boost1 = HPBoost()
            if event.type == SPEEDUP:  # прошло время ускорения
                player.speed = SHIP_SPEED
            if event.type == SPEEDUPCD:  # прошло кд и можно опять использовать ускорение
                speed_boost = False
                SPEEDBOOST = SpeedBoost(96, 96)
            if laser_time_change:
                alarm_time = random.randint(10000, 20000)  # спавнит предупреждение о лазере от 10 до 20 сек
                pygame.time.set_timer(ALARM, alarm_time)
                pygame.time.set_timer(LASERSPAWN, alarm_time + 2000)
                pygame.time.set_timer(LASERDELETE, alarm_time + 6000)
                laser_time_change = False
            if event.type == ALARM:
                alarm_sound.play()
                laser_y = random.randint(32, screen_height - 32)  # случайная y для лазера
                alarm = Alarm(laser_y + 32)
            if event.type == LASERSPAWN:
                alarm.kill()
                laser_sound.play()
                laser1 = Laser(laser_y)
            if event.type == LASERDELETE:
                laser1.kill()
                laser_time_change = True
            if not enemy_sprites:
                if wave1:
                    wave1 = False
                    enemy0 = EnemyShip(300, 300, 1, 2, player, enemy_sprites)
                    enemy1 = EnemyShip(1000, 300, -1, 2, player, enemy_sprites)
                    enemy2 = EnemyShip(1600, 300, 1, 2, player, enemy_sprites)
                    big1 = BigEnemyShip(500, 0, 1, 3, player, enemy_sprites)
                    big2 = BigEnemyShip(1300, 0, -1, 3, player, enemy_sprites)
                    wave2 = True
                elif wave2:
                    wave2 = False
                    enemy0 = EnemyShip(300, 300, 1, 2, player, enemy_sprites)
                    enemy1 = EnemyShip(1000, 300, -1, 2, player, enemy_sprites)
                    enemy2 = EnemyShip(1600, 300, 1, 2, player, enemy_sprites)
                    rocket1 = Rocket(100, 100, player, all_sprites)
                    rocket2 = Rocket(400, 100, player, all_sprites)
                    rocket3 = Rocket(800, 100, player, all_sprites)
                    rocket4 = Rocket(1500, 100, player, all_sprites)
                    big1 = BigEnemyShip(screen_width // 2, 0, -1, 3, player, enemy_sprites)
                    wave3 = True
                elif wave3:
                    wave3 = False
                    enemy0 = EnemyShip(300, 100, -1, 2, player, enemy_sprites)
                    enemy1 = EnemyShip(500, 300, 1, 2, player, enemy_sprites)
                    enemy2 = EnemyShip(800, 100, -1, 2, player, enemy_sprites)
                    enemy3 = EnemyShip(1200, 300, 1, 2, player, enemy_sprites)
                    enemy4 = EnemyShip(1600, 100, -1, 2, player, enemy_sprites)
                    enemy5 = EnemyShip(1800, 300, 1, 2, player, enemy_sprites)
                    rocket = Rocket(400, 200, player, all_sprites)
                    rocket2 = Rocket(800, 200, player, all_sprites)
                    small1 = SmallEnemy(350, 200, 1, 1, player, enemy_sprites)
                    small2 = SmallEnemy(1300, 400, -1, 1, player, enemy_sprites)
                    wave4 = True
                elif wave4:
                    wave4 = False
                    enemy0 = EnemyShip(300, 100, -1, 2, player, enemy_sprites)
                    enemy1 = EnemyShip(500, 300, 1, 2, player, enemy_sprites)
                    small1 = SmallEnemy(500, 300, -1, 1, player, enemy_sprites)
                    small2 = SmallEnemy(900, 400, 1, 1, player, enemy_sprites)
                    small3 = SmallEnemy(1200, 300, -1, 1, player, enemy_sprites)
                    small4 = SmallEnemy(1600, 200, 1, 1, player, enemy_sprites)
                    rocket = Rocket(400, 200, player, all_sprites)
                    rocket2 = Rocket(800, 200, player, all_sprites)
                    rocket3 = Rocket(1200, 200, player, all_sprites)
                    rocket4 = Rocket(1800, 200, player, all_sprites)
                    big1 = BigEnemyShip(600, 0, 1, 3, player, enemy_sprites)
                    big2 = BigEnemyShip(1000, 0, -1, 3, player, enemy_sprites)
                    big3 = BigEnemyShip(1800, 0, -1, 3, player, enemy_sprites)
                    big4 = BigEnemyShip(100, 0, 1, 3, player, enemy_sprites)
        # проверка на потерю хп чтобы удалить спрайты
        hp_count = my_font.render(str(player.hp), False, (255, 255, 255))
        points_count = my_font.render(str(score.score), False, (255, 255, 255))
        all_sprites.update()
        enemy_sprites.update()
        boosts_sprites.update()
        screen.fill('black')
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        boosts_sprites.draw(screen)
        screen.blit(hp_count, (64, 16))
        screen.blit(points_count, (192, 16))
        pygame.display.flip()
        clock.tick(FPS)


def boss_level(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites, boosts_sprites,boss_sprite, my_font):
    running = True
    shooting = False
    can_shoot = True
    speed_boost = False
    died = False

    # События и таймеры босса
    BOSSLASER = pygame.USEREVENT + 11
    BOSSLASERDELETE = pygame.USEREVENT + 12
    BOSSBOUNCESHOOTING = pygame.USEREVENT + 13
    ROCKETSPAWN = pygame.USEREVENT + 14

    pygame.time.set_timer(BOSSLASER, 1000) # кд лазера
    pygame.time.set_timer(BOSSLASERDELETE, 2000) # сколько он действует
    laser_boss_cd = False
    pygame.time.set_timer(BOSSBOUNCESHOOTING, 750)
    pygame.time.set_timer(ROCKETSPAWN, 4500)

    pygame.time.set_timer(ENEMYSHOOTING, 750)
    pygame.time.set_timer(CHANGEENEMYDIR, 500)
    pygame.time.set_timer(HPBOOSTSPAWN, 15000)
    pygame.time.set_timer(SPEEDUP, 0)
    pygame.time.set_timer(SPEEDUPCD, 0)
    alarm_time = random.randint(5000, 10000)  # спавнит предупреждение о лазере от 10 до 20 сек
    pygame.time.set_timer(ALARM, alarm_time)
    pygame.time.set_timer(LASERSPAWN, alarm_time + 2000)
    pygame.time.set_timer(LASERDELETE, alarm_time + 4000)
    laser_time_change = False
    # Интерфейс
    HP1 = HP(128, 16)
    POINTS = Points(272, 16)
    SPEEDBOOST = SpeedBoost(96, 96)

    player = MainShip(all_sprites, player_sprite)
    #enemy0 = EnemyShip(50, 200, 1, 2, player, enemy_sprites)
    #enemy2 = EnemyShip(400, 200, -1, 2, player, enemy_sprites)
    #enemy3 = EnemyShip(1500, 200, -1, 2, player, enemy_sprites)
    #enemy4 = EnemyShip(1900, 200, 1, 2, player, enemy_sprites)
    boss = Boss(screen_width // 2, 200, 2, player, boss_sprite)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            player.handle_input(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shooting = True
                if event.key == pygame.K_LSHIFT:
                    if not speed_boost:  # проверяем прошло ли кд
                        SPEEDBOOST.kill()
                        player.speed += 5  # увеличиваем скорость и запускаем таймера
                        pygame.time.set_timer(SPEEDUP, 3000)
                        pygame.time.set_timer(SPEEDUPCD, 6000)
                        speed_boost = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    shooting = False
            # Выстрел
            if event.type == SHOOTCD:
                can_shoot = True

            if event.type == DIEANIM:
                died = True

            if player.hp <= 0:
                player.kill()
                pygame.time.set_timer(DIEANIM, 200)
                if died:
                    for x in all_sprites, enemy_sprites, boosts_sprites, boss_sprite:
                        for y in x:
                            y.kill()
                    return "lose"

            if shooting and can_shoot:
                player.main_ship_shooting()
                sound_shoot.play()
                pygame.time.set_timer(SHOOTCD, 500)  # запуск кд на выстрел
                can_shoot = False
            # События БОССА

            if laser_boss_cd:
                if boss.phase == 1:
                    pygame.time.set_timer(BOSSLASER,1000)
                    pygame.time.set_timer(BOSSLASERDELETE, 2000)
                else:
                    pygame.time.set_timer(BOSSLASER, 0)
                    pygame.time.set_timer(BOSSLASERDELETE, 0)
                laser_boss_cd = False
            if event.type == BOSSLASER:
                if boss_sprite and boss.moved and boss.phase == 1:
                    boss.laser_attack()
            if event.type == BOSSLASERDELETE:
                boss.laser.kill()
                boss.moved = False
                laser_boss_cd = True
            if event.type == BOSSBOUNCESHOOTING and boss.phase == 2:
                boss.bounce_attack()
            if event.type == ROCKETSPAWN and boss.phase == 2:
                rocket = Rocket(400, 200, player, all_sprites)
                rocket2 = Rocket(screen_width - 400, 200, player, all_sprites)
            # События
            if event.type == ENEMYSHOOTING:
                for enemy in enemy_sprites:
                    enemy.enemy_shooting()
            if event.type == CHANGEENEMYDIR:  # меняет направление
                for enemy in enemy_sprites:
                    if enemy.change_dir:
                        enemy.changeDir()
            if event.type == HPBOOSTSPAWN:
                hp_boost1 = HPBoost()
            if event.type == SPEEDUP:  # прошло время ускорения
                player.speed = SHIP_SPEED
            if event.type == SPEEDUPCD:  # прошло кд и можно опять использовать ускорение
                speed_boost = False
                SPEEDBOOST = SpeedBoost(96, 96)
            if laser_time_change:
                alarm_time = random.randint(5000, 10000)  # спавнит предупреждение о лазере от 10 до 20 сек
                pygame.time.set_timer(ALARM, alarm_time)
                pygame.time.set_timer(LASERSPAWN, alarm_time + 2000)
                pygame.time.set_timer(LASERDELETE, alarm_time + 4000)
                laser_time_change = False
            if event.type == ALARM:
                alarm_sound.play()
                laser_y1 = random.randint(32, screen_height - 32)  # случайная y для лазера
                laser_y2 = random.randint(32, screen_height - 32)  # случайная y для лазера
                alarm = Alarm(laser_y1 + 32)
                alarm2 = Alarm(laser_y2 + 32)
            if event.type == LASERSPAWN:
                alarm.kill()
                alarm2.kill()
                laser_sound.play()
                laser1 = Laser(laser_y1)
                laser2 = Laser(laser_y2)
            if event.type == LASERDELETE:
                laser1.kill()
                laser2.kill()
                laser_time_change = True

        # проверка на потерю хп чтобы удалить спрайты
        hp_count = my_font.render(str(player.hp), False, (255, 255, 255))
        points_count = my_font.render(str(score.score), False, (255, 255, 255))
        all_sprites.update()
        enemy_sprites.update()
        boosts_sprites.update()
        boss_sprite.update()
        screen.fill('black')
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        boosts_sprites.draw(screen)
        boss_sprite.draw(screen)
        screen.blit(hp_count, (64, 16))
        screen.blit(points_count, (192, 16))
        pygame.display.flip()
        clock.tick(FPS)
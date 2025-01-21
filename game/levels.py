import pygame, random
from classes import MainShip, EnemyShip, Bullet, HPBoost, HP, BigEnemyShip, Rocket, player_sprite, Laser, Alarm, \
    SmallEnemy
from config import MUSIC_VOLUME, EFFECT_VOLUME

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
CHANGEENEMYDIR = pygame.USEREVENT + 9 # событие смены направления мальнького кораблся

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

# Интерфейс
HP1 = HP(128, 16)


# Первый левел(он не такой должен быть это к примеру)
def level_one(screen, clock, FPS, screen_width, screen_height, all_sprites, enemy_sprites, boosts_sprites, my_font):
    running = True
    shooting = False
    can_shoot = True
    speed_boost = False

    pygame.time.set_timer(ENEMYSHOOTING, 500)
    pygame.time.set_timer(CHANGEENEMYDIR, 500)
    pygame.time.set_timer(HPBOOSTSPAWN, 15000)
    pygame.time.set_timer(SPEEDUP, 0)
    pygame.time.set_timer(SPEEDUPCD, 0)
    alarm_time = random.randint(10000, 20000)  # спавнит предупреждение о лазере от 10 до 20 сек
    pygame.time.set_timer(ALARM, alarm_time)
    pygame.time.set_timer(LASERSPAWN, alarm_time + 2000)
    pygame.time.set_timer(LASERDELETE, alarm_time + 6000)
    laser_time_change = False

    player = MainShip(all_sprites, player_sprite)
    enemy1 = EnemyShip(300, 200, 1, 2, enemy_sprites)  # x, y, x_dir, attack_speed(чем больше тем медленее), spriteGroup
    enemy2 = EnemyShip(900, 200, -1, 2, enemy_sprites)  # также есть скрытый параметр change_dir=False
    enemy3 = BigEnemyShip(300, 200, 1, 3, enemy_sprites)
    rocket = Rocket(100, 100, player, all_sprites)
    small = SmallEnemy(200, 200, 1, 1, enemy_sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shooting = True
                if event.key == pygame.K_LSHIFT:
                    if not speed_boost:  # проверяем прошло ли кд
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

        # проверка на потерю хп чтобы удалить спрайты
        hp_count = my_font.render(str(player.hp), False, (255, 255, 255))
        all_sprites.update()
        enemy_sprites.update()
        boosts_sprites.update()
        screen.fill('black')
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        boosts_sprites.draw(screen)
        screen.blit(hp_count, (64, 16))
        pygame.display.flip()
        clock.tick(FPS)

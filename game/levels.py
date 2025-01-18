import pygame
from classes import MainShip, EnemyShip, Bullet, HPBoost, HP, BigEnemyShip, Rocket, player_sprite
from config import MUSIC_VOLUME, EFFECT_VOLUME

# Глоб переменные
SHIP_SPEED = 5
SHOOTCD = pygame.USEREVENT + 1
ENEMYSHOOTING = pygame.USEREVENT + 2
HPBOOSTSPAWN = pygame.USEREVENT + 3
SPEEDUP = pygame.USEREVENT + 4
SPEEDUPCD = pygame.USEREVENT + 5

# Музыка и звуки(файла нет(
pygame.mixer.music.load('data\\Sounds\\BackSound.ogg')
sound_shoot = pygame.mixer.Sound('data\\Sounds\\Shoot.wav')
sound_shoot.set_volume(EFFECT_VOLUME)
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

    pygame.time.set_timer(ENEMYSHOOTING, 1000)
    pygame.time.set_timer(HPBOOSTSPAWN, 15000)
    pygame.time.set_timer(SPEEDUP, 0)
    pygame.time.set_timer(SPEEDUPCD, 0)

    player = MainShip(all_sprites, player_sprite)
    enemy1 = EnemyShip(300, 200, 1, enemy_sprites)
    enemy2 = EnemyShip(900, 200, -1, enemy_sprites)
    enemy3 = BigEnemyShip(300, 200, 1, enemy_sprites)
    rocket = Rocket(100, 100, player, all_sprites)

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
                sound_shoot.play()  # пока музыки нет (
                pygame.time.set_timer(SHOOTCD, 500)  # запуск кд на выстрел
                can_shoot = False
            # События
            if event.type == ENEMYSHOOTING:
                for enemy in enemy_sprites:
                    enemy.enemy_shooting()
            if event.type == HPBOOSTSPAWN:
                hp_boost1 = HPBoost()
            if event.type == SPEEDUP:  # прошло время ускорения
                player.speed = SHIP_SPEED
            if event.type == SPEEDUPCD:  # прошло кд и можно опять использовать ускорение
                speed_boost = False

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

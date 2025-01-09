from classes import MainShip, Bullet, EnemyShip, HP, HPBoost, SHIP_SPEED
from classes import all_sprites, enemy_sprites, bullets_sprites, boosts_sprites
from config import size, screen_width, screen_height, FPS
import pygame

# переменные
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 40)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player = MainShip(all_sprites)
enemy1 = EnemyShip(screen_width - 100, 200, 1, enemy_sprites)
enemy2 = EnemyShip(screen_width // 2, 200, -1, enemy_sprites)
enemy3 = EnemyShip(300, 200, 1, enemy_sprites)

# Интерфейс
HP1 = HP(128, 16)
# событие выстрела
ENEMYSHOOTING = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYSHOOTING, 1000)
# событие появления хилки
HPBOOSTSPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(HPBOOSTSPAWN, 10000)
# ускорение
SPEEDUP = pygame.USEREVENT + 3
SPEEDUPCD = pygame.USEREVENT + 4
speed_boost = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.main_ship_shooting()
            if event.key == pygame.K_LSHIFT:
                if not speed_boost:  # проверяем прошло ли кд
                    player.speed += 5  # увеличиваем скорость и запускаем таймера
                    pygame.time.set_timer(SPEEDUP, 3000)
                    pygame.time.set_timer(SPEEDUPCD, 6000)
                    speed_boost = True
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
    bullets_sprites.draw(screen)
    enemy_sprites.draw(screen)
    boosts_sprites.draw(screen)
    screen.blit(hp_count, (64, 16))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

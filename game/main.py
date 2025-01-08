from classes import MainShip, Bullet, EnemyShip
from classes import all_sprites, enemy_sprites, bullets_sprites
import pygame

FPS = 40
pygame.init()
# получаем информацию о дисплее
info = pygame.display.Info()
screen_width = info.current_w - 100
screen_height = info.current_h - 100
size = screen_width, screen_height

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
player = MainShip(screen_width, screen_height, all_sprites)
enemy1 = EnemyShip(screen_width - 100, 200, 1, screen_width, screen_height, enemy_sprites)
enemy2 = EnemyShip(screen_width // 2, 200, 1, screen_width, screen_height, enemy_sprites)
enemy3 = EnemyShip(300, 200, 1, screen_width, screen_height, enemy_sprites)
# событие выстрела
ENEMYSHOOTING = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMYSHOOTING, 1000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top, screen_width, screen_height, all_sprites,
                                bullets_sprites)
        if event.type == ENEMYSHOOTING:
            for enemy in enemy_sprites:
                enemy.enemy_shooting()
    all_sprites.update()
    enemy_sprites.update()
    screen.fill('black')
    all_sprites.draw(screen)
    bullets_sprites.draw(screen)
    enemy_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


from classes import MainShip, Bullet
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
all_sprites = pygame.sprite.Group()
player = MainShip(screen_width, screen_height, all_sprites)
bullets = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top, screen_width, screen_height,all_sprites, bullets )

    all_sprites.update()
    screen.fill('black')
    all_sprites.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
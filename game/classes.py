import os
import sys
import pygame

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
        self.speed = 5

    def update(self, *args):
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w]:
          self.rect.y -= self.speed
      if keys[pygame.K_s]:
          self.rect.y += self.speed
      if keys[pygame.K_a]:
          self.rect.x -= self.speed
      if keys[pygame.K_d]:
          self.rect.x += self.speed
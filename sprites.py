from random import randint

import pygame.sprite

from load_images import load_image


class Static_Block(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, width, height):
        super().__init__(*group)
        self.image = pygame.Surface((width, height))
        photo = load_image('1.jpg')
        self.image.blit(photo, (0, 0), (randint(0, photo.get_width() - width), randint(0, photo.get_height() - height),
                                        width, height))
        pygame.draw.rect(self.image, pygame.Color(randint(0, 255), randint(0, 255), randint(0, 255)),
                         (0, 0, width, height), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Move_Block(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, width, height):
        super().__init__(*group)
        self.image = pygame.Surface((width, height))
        photo = load_image('1.jpg')
        self.image.blit(photo, (0, 0), (randint(0, photo.get_width() - width), randint(0, photo.get_height() - height),
                                        width, height))
        pygame.draw.rect(self.image, pygame.Color(randint(0, 255), randint(0, 255), randint(0, 255)),
                         (0, 0, width, height), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.max_x = x
        self.rect.y = y
        self.dire = 1

    def move(self, dt):
        if self.rect.x == 0:
            self.dire *= -1
        elif self.rect.x == self.max_x - self.rect.width and self.dire == -1:
            self.dire *= -1
        if self.dire == 1:
            self.rect.x -= dt * 100
        else:
            self.rect.x += dt * 100


class Camera:
    def __init__(self):
        self.dy = 50

    def apply(self, obj):
        obj.rect.y += self.dy


class Rabbit(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, rotation):
        super().__init__(*group)
        photo = load_image('rabbits.png')
        self.image = pygame.Surface((800, 200))
        if rotation == 'c':
            new_image = pygame.Surface((30, 45))
            new_image.blit(photo, (0, 0), (0, 0,
                                              30, 45))
            new_image = pygame.transform.scale(new_image, (100, 200))
            self.image.blit(new_image, (350, 0), (0, 0, 100, 200))
        elif rotation == 'r':
            new_image = pygame.Surface((30, 50))
            new_image.blit(photo, (0, 0), (30, 145,
                                           30, 50))
            new_image = pygame.transform.scale(new_image, (100, 200))
            self.image.blit(new_image, (600, 0), (0, 0, 100, 200))
        else:
            new_image = pygame.Surface((30, 50))
            new_image.blit(photo, (0, 0), (60, 96,
                                           30, 50))
            new_image = pygame.transform.scale(new_image, (100, 200))
            self.image.blit(new_image, (50, 0), (0, 0, 100, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


class Carrot(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        photo = load_image('new.png')
        self.image = pygame.Surface((880, 350))
        self.image.blit(photo, (0, 0), (100, 380, 880, 350))
        self.image = pygame.transform.scale(self.image, (176, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

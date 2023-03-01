import sys
import time
from random import randint

import pygame as pygame

from load_images import load_image
from sprites import Static_Block, Camera, Move_Block, Rabbit, Carrot

pygame.init()


def collide_by_side(static_tile, move_tile):
    left = max(static_tile.rect.x, move_tile.rect.x)
    right = min(static_tile.rect.x + static_tile.rect.width, move_tile.rect.x + move_tile.rect.width)
    if static_tile.rect.x > move_tile.rect.x + move_tile.rect.width or \
            static_tile.rect.x + static_tile.rect.width < move_tile.rect.x:
        return
    return left, right


def eq_x(static_tile, carrot):
    if static_tile.rect.x + static_tile.rect.width < carrot.rect.x:
        return 'r', 600
    elif carrot.rect.x + carrot.rect.width < static_tile.rect.x:
        return 'l', 50
    return 'c', 350


class Game:
    def __init__(self):
        self.sc = pygame.display.set_mode((800, 800))
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.fps = 80
        self.all_sprites = pygame.sprite.Group()
        self.rabbit_sprite = pygame.sprite.Group()
        self.curr = None
        self.prev = None
        self.rabbit = None
        self.carrot = None
        self.carrots = []
        self.COUNTER = 0

    def start_screen(self):
        # заставка
        intro_text = ["Wake up, Neo...", 'The Matrix has you...', "Follow the white rabbit..."]
        fon = pygame.transform.scale(load_image('bl.png'), (self.sc.get_width(), self.sc.get_height()))
        self.sc.blit(fon, (0, 0))
        font = pygame.font.Font('font.ttf', 30)
        curr_y = 200
        final_x = 0
        for line in intro_text:
            curr_x = 25
            for letter in line:
                string_rendered = font.render(letter, 1, pygame.Color('green'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = curr_y
                curr_x += intro_rect.width
                intro_rect.x = curr_x
                self.sc.blit(string_rendered, intro_rect)
                time.sleep(0)
                pygame.display.flip()
                final_x = curr_x + intro_rect.width
            curr_y += 40
        string_rendered = font.render('Press Space to start', 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 600
        intro_rect.x = 25
        self.sc.blit(string_rendered, intro_rect)
        pygame.display.flip()
        color = 0
        is_start = True
        # конец заставки, начало мигания курсора и ожидания начала игры
        while True:
            if is_start:
                if color:
                    image = pygame.Surface([17, 30])
                    image.fill(pygame.Color("black"))
                    self.sc.blit(image, (final_x, curr_y - 40))
                    color -= 1
                else:
                    image = pygame.Surface([17, 30])
                    image.fill(pygame.Color("green"))
                    self.sc.blit(image, (final_x, curr_y - 40))
                    color += 1
                time.sleep(0.4)
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    is_start = False
                    self.run()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        # объект камеры для адекватного перемещения экрана с движением блоков
        camera = Camera()
        last_time = time.time()
        # случайный выбор иксовых координат спавна морковок
        for i in range(1, 6):
            if i % 2 == 0:
                x = randint(self.sc.get_width() // 2, self.sc.get_width() - 150)
            else:
                x = randint(0, self.sc.get_width() // 2)
            self.carrots.append(Carrot([self.all_sprites], x=x, y=-camera.dy * i * 5 + camera.dy * 8))

        self.sc.fill('black')
        # начальные 2 блока
        self.prev = Static_Block([self.all_sprites], x=200, y=600, width=200, height=50)
        self.curr = Move_Block([self.all_sprites], x=self.sc.get_width(), y=self.prev.rect.y - self.prev.rect.height,
                               width=self.prev.rect.width, height=self.prev.rect.height)

        self.rabbit_sprite.empty()
        res = eq_x(self.prev, self.carrots[0])
        self.rabbit = Rabbit([self.rabbit_sprite], x=0, y=0, rotation=res[0])
        self.all_sprites.draw(self.sc)
        pygame.display.flip()
        # игровой цикл
        while True:

            self.sc.fill('black')

            dt = time.time() - last_time
            last_time = time.time()
            self.curr.move(dt)

            self.all_sprites.draw(self.sc)
            self.rabbit_sprite.draw(self.sc)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.curr.rect.y <= self.carrots[0].rect.y + self.carrots[0].rect.height:
                        self.COUNTER += pygame.sprite.collide_rect(self.curr, self.carrots[0])
                        if len(self.carrots) > 1:
                            self.all_sprites.remove(self.carrots[0])
                            self.carrots = self.carrots[1:]
                        else:
                            self.end()

                    self.sc.fill('black')

                    self.rabbit_sprite.empty()
                    res = eq_x(self.curr, self.carrots[0])
                    # self.rabbit = Rabbit([self.rabbit_sprite], x=res[1], y=100, rotation=res[0])
                    self.rabbit = Rabbit([self.rabbit_sprite], x=0, y=0, rotation=res[0])

                    for sprite in self.all_sprites:
                        camera.apply(sprite)

                    self.all_sprites.remove(self.curr)

                    func = collide_by_side(self.prev, self.curr)
                    if func:
                        self.prev = Static_Block([self.all_sprites], x=self.curr.rect.x, y=self.curr.rect.y,
                                                 width=self.curr.rect.width, height=self.curr.rect.height)
                        self.curr = Move_Block([self.all_sprites], x=self.sc.get_width(),
                                               y=self.prev.rect.y - self.prev.rect.height,
                                               width=self.prev.rect.width, height=self.prev.rect.height)
                    else:
                        self.end()
                    self.all_sprites.draw(self.sc)
                    self.rabbit_sprite.draw(self.sc)
                    pygame.display.flip()
            self.clock.tick(self.fps)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def end(self):
        self.sc.fill((0, 0, 0))
        intro_text = ["Если Вы не поняли, во что поиграли, то объясняю:",
                      'В данной игре Вам нужно собирать морковки, ',
                      'следуя указаниям по направлению от белого кролика:',
                      "Куда он показывает, туда и надо строиться",
                      'Важно, чтобы каждый последующий тайл прикасался ',
                      'к предыдущему, иначе будет проигрыш',
                      'Ну и, как говориться напоследок: Git gud',
                      '',
                      "Press Space to restart"]
        font = pygame.font.Font('font.ttf', 25)
        text_coord = 400
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.sc.blit(string_rendered, intro_rect)
        string_rendered = font.render(f'Your Score: {self.COUNTER}', 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 200
        intro_rect.x = 100
        self.sc.blit(string_rendered, intro_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == 768:
                    self.sc = pygame.display.set_mode((800, 800))
                    pygame.display.flip()
                    self.clock = pygame.time.Clock()
                    self.fps = 80
                    self.all_sprites = pygame.sprite.Group()
                    self.rabbit_sprite = pygame.sprite.Group()
                    self.curr = None
                    self.prev = None
                    self.rabbit = None
                    self.carrot = None
                    self.carrots = []
                    self.COUNTER = 0
                    self.start_screen()


if __name__ == '__main__':
    game = Game()
    game.start_screen()

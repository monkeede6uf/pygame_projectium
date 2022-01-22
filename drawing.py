import pygame
from settings import *
from map import mini_map


class Drawing:
    def __init__(self, sc, sc_map, sc_stm, sc_gun):
        self.sc = sc
        self.sc_map = sc_map
        self.sc_stm = sc_stm
        self.sc_gun = sc_gun
        self.font_text = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_num = pygame.font.SysFont('Arial', 100, bold=True)
        self.counter = 0
        self.textures = {1: pygame.image.load('data/11.png').convert(),
                         2: pygame.image.load('data/12.png').convert(),
                         21: pygame.image.load('data/21.png').convert(),
                         22: pygame.image.load('data/22.png').convert(),
                         'sky': pygame.image.load('data/sky.png').convert(),
                         'ship': pygame.image.load('data/ship.png').convert(),
                         'logo': pygame.image.load('data/logo.png').convert_alpha(),
                         'book': [pygame.image.load(f'data/knigga/{i}.png').convert_alpha() for i in range(2)],
                         'pushka': [pygame.image.load(f'data/gun/{i}.png').convert_alpha() for i in range(13)],
                         'boom': pygame.image.load('data/boom.png').convert_alpha(),
                         'stamina': pygame.image.load('data/stamina.png').convert_alpha(),
                         'health': pygame.image.load('data/health.png').convert_alpha()}

    def start(self, res):
        self.sc.fill((106, 197, 244))
        self.sc.blit(self.textures['logo'], (300, 50))
        pygame.draw.rect(self.sc, (255, 255, 255), (230, 590, 735, 65), 0)
        tx = self.font_text.render('Нажмите на любую клавишу, чтобы продолжить', 1, (255, 92, 0))
        self.sc.blit(tx, (245, 600))
        pos = 100
        for i in res:
            self.sc.blit(self.font_text.render(i + 's' if i != 'Your records:' else i, 1, WHITE), (950, pos))
            pos += 40

    def finish(self, time):
        self.sc.fill((106, 197, 244))
        render = self.font_num.render(f'{time.ljust(len(time[0:time.find(".")]) + 3, "0")}s', 1, WHITE)
        self.sc.blit(render, (WIDTH // 2 - 100,  HEIGHT // 3 + 20))
        render = self.font_text.render('Вы прошли игру, время прохождения составило:', 1, (255, 92, 0))
        pygame.draw.rect(self.sc, (255, 255, 255), (235, 235, 745, 65), 0)
        self.sc.blit(render, (247, HEIGHT // 3 - 20))

    def background(self, angle, player_level):
        key = 'sky' if player_level == 'paradise' else 'ship'
        col = DARKGRAY if player_level == 'space_ship' else SANDY
        sky_offset = -7 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures[key], (sky_offset, 0))
        self.sc.blit(self.textures[key], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures[key], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, col, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, sprite, sprite_pos = obj
                self.sc.blit(sprite, sprite_pos)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font_num.render(display_fps, 0, RED)
        self.sc.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                               map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, RED, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, (117, 246, 255), (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)

    def stamina(self, player_stamina):
        pygame.draw.rect(self.sc_stm, WHITE, (0, 0, 200, 20))
        pygame.draw.rect(self.sc_stm, VYRVI_GLAZ, (0, 0, 200 - player_stamina, 20))
        self.sc.blit(self.sc_stm, STAMINA_POS)
        self.sc.blit(self.textures['stamina'], (210, 15))

    def health(self, hp):
        pygame.draw.rect(self.sc_stm, WHITE, (0, 0, 200, 20))
        pygame.draw.rect(self.sc_stm, RED, (0, 0, 200 - hp, 20))
        self.sc.blit(self.sc_stm, HP_POS)
        self.sc.blit(self.textures['health'], (210, 45))

    def gun(self, level, time):
        self.sc.blit(self.textures['book' if level == 'paradise' else 'pushka'][self.counter], PUSHKA_POS)
        if time < 0.17 and self.counter < len(self.textures['book' if level == 'paradise' else 'pushka']) - 1:
            self.counter += 1
        else:
            self.counter = 0

    def boom(self, dist):
        image_scaled = pygame.transform.scale(self.textures['boom'],
                                              (self.textures['boom'].get_width() * dist,
                                               self.textures['boom'].get_height() * dist))
        self.sc.blit(image_scaled, (WIDTH // 2 - (image_scaled.get_width() // 2),
                                    HEIGHT // 2 - (image_scaled.get_height() // 2)))


class Gif:
    def __init__(self, sc):
        self.counter = 0
        self.sc = sc
        self.gif = [pygame.image.load(f'data/gif/{i}.png').convert_alpha() for i in range(1, 34)]

    def change_gif(self):
        self.sc.blit(self.gif[self.counter], (0, 0))
        self.counter += 1 if self.counter < len(self.gif) else 0

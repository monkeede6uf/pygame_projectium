import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map


class Drawing:
    def __init__(self, sc, sc_map, sc_stm, sc_gun):
        self.sc = sc
        self.sc_map = sc_map
        self.sc_stm = sc_stm
        self.sc_gun = sc_gun
        self.font_text = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_num = pygame.font.SysFont('Arial', 100, bold=True)
        self.textures = {1: pygame.image.load('data/11.png').convert(),
                         2: pygame.image.load('data/12.png').convert(),
                         21: pygame.image.load('data/21.png').convert(),
                         22: pygame.image.load('data/22.png').convert(),
                         'sky': pygame.image.load('data/sky.png').convert(),
                         'ship': pygame.image.load('data/ship.png').convert(),
                         'logo': pygame.image.load('data/logo.png').convert_alpha(),
                         'book': pygame.image.load('data/nigga.png').convert_alpha(),
                         'pushka': pygame.image.load('data/gun.png').convert_alpha()
                         }

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
        sky_offset = -7 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures[key], (sky_offset, 0))
        self.sc.blit(self.textures[key], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures[key], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, player_pos, player_angle, player_level):
        ray_casting(self.sc, player_pos, player_angle, self.textures, player_level)

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

    def stamina(self, player):
        pygame.draw.rect(self.sc_stm, WHITE, (0, 0, 200, 20))
        pygame.draw.rect(self.sc_stm, VYRVI_GLAZ, (0, 0, 200 - player.stamina, 20))
        self.sc.blit(self.sc_stm, STAMINA_POS)

    def gun(self, player):
        self.sc.blit(self.textures['book' if player.level == 'paradise' else 'pushka'], PUSHKA_POS)


class Gif:
    def __init__(self, sc):
        self.counter = 0
        self.sc = sc
        self.gif = [pygame.image.load(f'data/gif/{i}.png').convert_alpha() for i in range(1, 18)]

    def change_gif(self):
        self.sc.blit(self.gif[self.counter], (0, 0))
        self.counter += 1 if self.counter < len(self.gif) else 0
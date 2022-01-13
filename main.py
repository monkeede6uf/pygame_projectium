import pygame
from settings import *
from player import Player
import math
from drawing import Drawing, Gif

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE + 100, HEIGHT // MAP_SCALE))
sc_stm = pygame.Surface((200, 20))
sc_gun = pygame.Surface((500, 300))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, sc_map, sc_stm, sc_gun)
gif = Gif(sc)
pygame.mixer.music.load('data/main_theme.mp3')
game_started = False
fps = 80

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if not game_started and any(pygame.key.get_pressed()):
            game_started = True
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)
    if game_started:
        player.movement()
        sc.fill(BLACK)
        drawing.background(player.angle, player.level)
        drawing.world(player.pos, player.angle, player.level)
        drawing.stamina(player)
        drawing.gun(player)
        if player.map:
            drawing.mini_map(player)
        if player.level_changed and gif.counter < len(gif.gif) - 1:
            fps = 7
            gif.change_gif()
        else:
            fps = 80
    else:
        drawing.start()

    pygame.display.flip()
    clock.tick(fps)
import pygame
from settings import *
from player import Player
import math
from map import world_map
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
sc_stm = pygame.Surface((200, 20))
sc_gun = pygame.Surface((500, 300))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, sc_map, sc_stm, sc_gun)
pygame.mixer.music.load('data/main_theme.mp3')
game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if not game_started and any(pygame.key.get_pressed()):
            game_started = True
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
    if game_started:
        player.movement()
        sc.fill(BLACK)

        drawing.background(player.angle)
        drawing.world(player.pos, player.angle)
        drawing.stamina(player)
        drawing.gun(player)
    else:
        drawing.start()

    pygame.display.flip()
    clock.tick(80)
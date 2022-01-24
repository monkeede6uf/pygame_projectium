import pygame
from settings import *
from player import Player
import time
import csv
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing, Gif


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE + 100, HEIGHT // MAP_SCALE))
sc_stm = pygame.Surface((200, 20))
sc_gun = pygame.Surface((500, 300))
clock = pygame.time.Clock()
player = Player()
pygame.mouse.set_visible(False)
drawing = Drawing(sc, sc_map, sc_stm, sc_gun)
gif = Gif(sc)
sprites = Sprites()

pygame.mixer.music.load('data/main_theme.mp3')
shoots = {'paradise': pygame.mixer.Sound('data/sounds/book.wav'),
          'space_ship': pygame.mixer.Sound('data/sounds/laser_gun.wav')}

fps, start_time, timer = 80, 0, 0
with open('data/results.csv', encoding='utf-8') as f:
    old_results = sorted([i[0] for i in list(csv.reader(f, delimiter=';'))], key=lambda x: float(x))
    old_results = ['Your records:'] + old_results


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if player.game_moment == 'start' and any(pygame.key.get_pressed()):
            player.game_moment = 'paradise'
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.02)
            start_time = time.time()

    if player.game_moment in ['paradise', 'space_ship']:
        player.movement()
        sc.fill(BLACK)
        drawing.background(player.angle, player.level)
        walls = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects[player.level]])
        drawing.stamina(player)
        drawing.gun(player)
        sprites.check_health(player)
        closest = sprites.return_closest(player)
        if player.shoot(closest):
            shoots[player.level].play()
            drawing.boom(0.5)

        if player.map:
            drawing.mini_map(player)

        if player.game_moment == 'space_ship' and gif.counter < len(gif.gif) - 1:
            fps = 7
            gif.change_gif()
        else:
            fps = 80
    elif player.game_moment == 'start':
        drawing.start(old_results[0:7])

    elif player.game_moment == 'finish':
        if timer == 0:
            timer = time.time() - start_time
            with open('data/results.csv', 'a', encoding='utf-8', newline='') as f:
                writ = csv.writer(f, delimiter=';')
                writ.writerow([str(round(timer, 2)).ljust(len(str(timer)[0:str(timer).find('.')]) + 3, '0')])
        drawing.finish(str(round(timer, 2)))

    pygame.display.flip()
    clock.tick(fps)

import pygame
from settings import *
from player import Player
import math
import time
import csv
from sprite_objects import *
from ray_casting import ray_casting
from drawing import Drawing, Gif

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# инициализация вспомогательных классов

sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface((WIDTH // MAP_SCALE + 100, HEIGHT // MAP_SCALE))
sc_stm = pygame.Surface((200, 20))
sc_gun = pygame.Surface((500, 300))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(sc, sc_map, sc_stm, sc_gun)
gif = Gif(sc)
sprites = Sprites()
pygame.mouse.set_visible(False)

# загрузка музыки

pygame.mixer.music.load('data/main_theme.mp3')
shoots = {'paradise': pygame.mixer.Sound('data/sounds/book.wav'),
          'space_ship': pygame.mixer.Sound('data/sounds/laser_gun.wav')}

fps, start_time, timer = 80, 0, 0

# получение предыдущих рекордов игрока

with open('data/results.csv', encoding='utf-8') as f:
    old_results = sorted([i[0] for i in list(csv.reader(f, delimiter=';'))], key=lambda x: float(x))
    old_results = ['Your records:'] + old_results


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            exit()
        # закрытие открытых меню с помощью нужных клавиш
        if player.game_moment == 'start' and any(pygame.key.get_pressed()):
            player.game_moment = 'paradise'
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.09)
            start_time = time.time()

        if player.game_moment == 'dead' and pygame.key.get_pressed()[pygame.K_r]:
            player.game_moment = player.level
            player.hp = 0
            player.x = 138
            player.y = 138
            player.angle = 0

    if player.game_moment in ['paradise', 'space_ship']:
        player.movement()

        # отрисовка

        sc.fill(BLACK)
        drawing.background(player.angle, player.level)
        walls = ray_casting(player.pos, player.angle, drawing.textures, player.level)
        drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects[player.level]])
        drawing.stamina(player.stamina)
        drawing.health(player.hp)

        sprites.check_health(player.level)

        # действия со стороны спрайтов

        for obj in sprites.list_of_objects[player.level]:
            obj.move_sprites(player.x, player.y,
                             ray_casting_npc_player(obj.x, obj.y,  (player.x, player.y),
                                                    player.level))
            obj.shoot(player, ray_casting_npc_player(obj.x, obj.y,  (player.x, player.y), player.level))
        closest = sprites.return_closest(player.level)
        if player.shoot(closest) and time.time() - player.last_shoot_time < 0.02:
            shoots[player.level].set_volume(0.1)
            shoots[player.level].play()
            drawing.boom(0.3)
        drawing.gun(player.level, time.time() - player.last_shoot_time)
        if player.map:
            drawing.mini_map(player)

            # отрисовка мини-карты

        # отрисовка анимации переключения уровня

        if player.game_moment == 'space_ship' and gif.counter < len(gif.gif) - 1:
            fps = 5
            gif.change_gif()
        else:
            fps = 80

        if player.hp >= 100:
            player.game_moment = 'dead'

    # отрисовка стартового и финишного меню
    elif player.game_moment == 'dead':
        drawing.dead()
    elif player.game_moment == 'start':
        drawing.start(old_results[0:7])
    elif player.game_moment == 'finish':
        if timer == 0:
            timer = time.time() - start_time

            # запись нынешнего результата игрока

            with open('data/results.csv', 'a', encoding='utf-8', newline='') as f:
                writ = csv.writer(f, delimiter=';')
                writ.writerow([str(round(timer, 2)).ljust(len(str(timer)[0:str(timer).find('.')]) + 3, '0')])
        drawing.finish(str(round(timer, 2)))
    pygame.display.flip()
    clock.tick(fps)

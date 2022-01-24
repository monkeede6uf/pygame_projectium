import pygame
from settings import *
from collections import deque
from ray_casting import ray_casting_npc_player
import time


class Sprites:
    def __init__(self):
        self.sprite_params = {
            'devil': {
                'sprite': pygame.image.load('data/sprites/chel.png').convert_alpha(),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/devil/{i}.png').convert_alpha() for i in range(9)]),
                'animation_speed': 10,
                'animation_dist': 700,
                'scale': 1,
                'vert': 0,
                'static': False},
            'space_devil': {
                'sprite': pygame.image.load('data/sprites/dev.png').convert_alpha(),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/devil1/{i}.png').convert_alpha() for i in range(4)]),
                'animation_speed': 15,
                'animation_dist': 700,
                'scale': 1,
                'vert': 0,
                'static': True},
            'angel_of_death': {
                'sprite': pygame.image.load('data/sprites/angel.png').convert_alpha(),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/devil2/{i}.png').convert_alpha() for i in range(12)]),
                'animation_speed': 20,
                'animation_dist': 700,
                'scale': 1,
                'vert': 0,
                'static': True},
            'flying_monster': {
                'sprite': pygame.image.load('data/sprites/fly.png').convert_alpha(),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/flying_monster/{i}.png').convert_alpha() for i in range(35)]),
                'animation_speed': 3,
                'animation_dist': 700,
                'scale': 1,
                'vert': 0,
                'static': True},
            }
        self.list_of_objects = {'paradise': [
            SpriteObject(self.sprite_params['devil'], (8, 7.5)),
            SpriteObject(self.sprite_params['angel_of_death'], (12, 6.4)),
            SpriteObject(self.sprite_params['angel_of_death'], (0, 0))
        ],
            'space_ship': [
                SpriteObject(self.sprite_params['space_devil'], (8, 7.5)),
                SpriteObject(self.sprite_params['flying_monster'], (12, 6.4))],
            'shot': []}

    def check_health(self, player_level):
        k = 0
        for i in range(len(self.list_of_objects[player_level])):
            if self.list_of_objects[player_level][i - k].hp <= 0:
                del self.list_of_objects[player_level][i]
                k += 1

    def return_closest(self, player_level):
        dp = sorted([obj for obj in self.list_of_objects[player_level] if obj.is_on_fire()],
                    key=lambda x: x.distance_to_sprite)
        return dp[0] if len(dp) != 0 else None

    def shoot(self, player_x, player_y, is_on_fire, closest):
        if len(self.list_of_objects['shot']) == 0 and is_on_fire:
            self.list_of_objects['shot'] = [SpriteObject(self.sprite_params['shot'], closest.pos), (player_x * SCALE, player_y * SCALE)]
            print(player_y, player_x)

        elif len(self.list_of_objects['shot']) > 0:
            pass



class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.static = parameters['static']
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = parameters['vert']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.stuck = parameters['static']

        self.hp = 100
        self.last_shoot_time = 0

    def object_locate(self, player, walls):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        if 0 <= self.current_ray <= NUM_RAYS - 1 and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.shift

            # анимация спрайта
            if self.animation and self.distance_to_sprite < self.animation_dist:
                self.object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (self.current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (self.proj_height, self.proj_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def affect(self):
        distance = self.get_dist()
        if 350 < int(distance) < 700:
            self.hp -= 20
        elif 280 < int(distance) < 350:
            self.hp -= 20
        elif 172 < int(distance) < 280:
            self.hp -= 30
        elif 75 < int(distance) < 172:
            self.hp -= 50

    def get_dist(self):
        return self.distance_to_sprite

    def is_on_fire(self):
        if CENTER_RAY - 50 < self.current_ray < CENTER_RAY + 50:
            return True
        return False

    def move_sprites(self, pl_x, pl_y, is_on_fire):
        if is_on_fire and self.distance_to_sprite > TILE and self.stuck:
            dx = self.x - pl_x
            dy = self.y - pl_y
            self.x = self.x + 1 if dx < 0 else self.x - 1
            self.y = self.y + 1 if dy < 0 else self.y - 1

    def shoot(self, player_class, is_on_fire):
        if is_on_fire and self.distance_to_sprite < 1.5 * TILE and time.time() - self.last_shoot_time > 1:
            player_class.hp += 10
            self.last_shoot_time = time.time()

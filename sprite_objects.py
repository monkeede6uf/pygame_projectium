import pygame
from settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_params = {
            'devil': {
                'sprite': pygame.image.load('data/sprites/0.png').convert_alpha(),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/devil/{i}.png').convert_alpha() for i in range(9)]),
                'animation_speed': 10,
                'animation_dist': 700,
                'scale': 1,
                'vert': 0,
                'static': True}
        }
        self.list_of_objects = {'paradise': [
            SpriteObject(self.sprite_params['devil'], (8, 7.5)),
            SpriteObject(self.sprite_params['devil'], (12, 6.4)),
        ],
            'space_ship': [
                SpriteObject(self.sprite_params['devil'], (8, 7.5)),
                SpriteObject(self.sprite_params['devil'], (12, 6.4)),
            ]}

    def check_health(self, player):
        k = 0
        for i in range(len(self.list_of_objects[player.level])):
            if self.list_of_objects[player.level][i - k].hp <= 0:
                del self.list_of_objects[player.level][i]
                k += 1

    def return_closest(self, player):
        sp = sorted(self.list_of_objects[player.level], key=lambda x: x.get_dist(player))
        if len(sp) != 0:
            return sp[0]
        else:
            return None


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

        self.hp = 100

    def object_locate(self, player, walls):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        if 0 <= current_ray <= NUM_RAYS - 1 and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            # sprite animation
            if self.animation and distance_to_sprite < self.animation_dist:
                self.object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def affect(self, player):
        distance = self.get_dist(player)
        if int(distance) in range(280, 350):
            self.hp -= 9
        elif int(distance) in range(172, 280):
            self.hp -= 20
        elif int(distance) in range(75, 172):
            self.hp -= 30

    def get_dist(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        return math.sqrt(dx ** 2 + dy ** 2)

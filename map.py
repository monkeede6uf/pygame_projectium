from settings import *
import pygame
from numba.core import types
from numba.typed import Dict
from numba import int32


text_map_paradise = [
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
    [11, 0, 0, 12, 0, 0, 0, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
    [11, 0, 11, 0, 0, 11, 0, 12, 11, 11, 11, 0, 12, 11, 11, 11, 11],
    [11, 0, 11, 0, 0, 11, 0, 12, 0, 11, 11, 0, 12, 11, 11, 11, 11],
    [11, 0, 11, 0, 11, 11, 0, 11, 0, 11, 11, 0, 12, 0, 0, 11, 11],
    [11, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11, 0, 12, 0, 0, 11, 11],
    [11, 0, 0, 0, 11, 11, 11, 0, 11, 11, 11, 0, 0, 0, 0, 11, 11],
    [11, 11, 11, 11, 11, 11, 11, 0, 0, 0, 0, 0, 12, 0, 0, 11, 11],
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 11, 11, 11, 11]
]

text_map_space_ship = [
    [21, 21, 22, 11, 21, 21, 21, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
    [22, 0, 0, 22, 0, 0, 0, 21, 11, 11, 11, 11, 11, 11, 11, 11, 11],
    [22, 0, 21, 0, 0, 21, 0, 22, 21, 21, 21, 0, 22, 21, 21, 21, 21],
    [22, 0, 21, 0, 0, 21, 0, 22, 0, 21, 21, 0, 21, 21, 21, 21, 22],
    [22, 0, 21, 0, 21, 21, 0, 21, 0, 21, 21, 0, 21, 0, 0, 21, 21],
    [21, 0, 0, 0, 0, 0, 0, 0, 0, 21, 21, 0, 21, 0, 0, 0, 22],
    [21, 0, 0, 0, 21, 21, 22, 0, 22, 21, 22, 0, 0, 0, 0, 21, 22],
    [21, 0, 21, 21, 21, 21, 22, 0, 0, 0, 0, 0, 22, 0, 0, 21, 22],
    [21, 21, 21, 22, 21, 11, 21, 22, 21, 21, 21, 21, 22, 22, 21, 21, 21]
]

WORLD_WIDTH = len(text_map_paradise[0]) * TILE
WORLD_HEIGHT = len(text_map_paradise) * TILE
all_levels = {}
mini_map = set()
all_collision_walls = {}
for level in [(text_map_paradise, 'paradise'), (text_map_space_ship, 'space_ship')]:
    world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_types=int32)
    collision_walls = []
    for j, row in enumerate(level[0]):
        for i, char in enumerate(row):
            if char != 0:
                collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                mini_map.add((i * MAP_TILE, j * MAP_TILE))
                if char == 11:
                    world_map[(i * TILE, j * TILE)] = 1
                elif char == 12:
                    world_map[(i * TILE, j * TILE)] = 2
                elif char == 21:
                    world_map[(i * TILE, j * TILE)] = 21
                elif char == 22:
                    world_map[(i * TILE, j * TILE)] = 22
    all_levels[level[1]] = world_map
    all_collision_walls[level[1]] = collision_walls

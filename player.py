from settings import *
import pygame
import math
from map import all_collision_walls

class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.stamina = 0
        self.regen = False
        self.level = 'paradise'
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)

    @property
    def pos(self):
        return self.x, self.y

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(all_collision_walls[self.level])

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = all_collision_walls[self.level][hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += next_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += next_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.rect.center = self.x, self.y

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d] :
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        if keys[pygame.K_LSHIFT]:
            if self.stamina <= 190:
                self.stamina += 3
                dx = player_speed * cos_a * 2
                dy = player_speed * sin_a * 2
                self.detect_collision(dx, dy)
            else:
                self.x += player_speed * cos_a
                self.y += player_speed * sin_a
        if not keys[pygame.K_LSHIFT]:
            self.stamina -= 1 if self.stamina > 0 else 0
        if keys[pygame.K_ESCAPE]:
            self.level = 'space_ship'


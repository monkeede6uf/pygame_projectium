from settings import *
import pygame
import math
import time
from map import all_collision_walls


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.stamina = 0
        self.regen = False
        self.level = 'paradise'
        self.side = 50
        self.map = False
        self.game_moment = 'start'
        self.rect = pygame.Rect(*player_pos, self.side, self.side)

        self.last_shoot_time = 0

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
            print(self.x, self.y, self.angle)
        if keys[pygame.K_m]:
            self.map = True if not self.map else False
        if int(self.x) in range(1324, 1404) and int(self.y) in range(425, 490) and self.level == 'paradise':
            self.level = 'space_ship'
            self.game_moment = 'space_ship'
            self.x = 243
            self.y = 148
            self.angle = -3.14
        if int(self.x) in range(1324, 1404) and int(self.y) in range(425, 490) and self.level == 'space_ship':
            self.game_moment = 'finish'

        if keys[pygame.K_j]:
            self.level = 'space_ship'
            self.game_moment = 'space_ship'
        if keys[pygame.K_k]:
            self.game_moment = 'finish'
        self.angle %= DOUBLE_PI

    def shoot(self, sprite):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and\
                time.time() - self.last_shoot_time > 0.5 and\
                sprite is not None:
            sprite.affect(self)
            self.last_shoot_time = time.time()
            return True
        elif keys[pygame.K_SPACE] and\
                time.time() - self.last_shoot_time > 0.4 and\
                sprite is None:
            self.last_shoot_time = time.time()
            return True
        else:
            return False

from settings import *
import pygame
import math
import time
from map import all_collision_walls


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.level = 'paradise'
        self.side = 50
        self.map = False
        self.game_moment = 'start'
        self.rect = pygame.Rect(*player_pos, self.side, self.side)

        self.last_shoot_time = 0
        self.last_resq_time = 0
        self.stamina = 0
        self.hp = 0
        self.sensitivity = 0.004

    @property
    def pos(self):
        return self.x, self.y

    # коллизия объекта и стен
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

    # движение игрока по карте

    def movement(self):
        self.keys_control()
        self.rect.center = self.x, self.y
        self.mouse_control()
        self.angle %= DOUBLE_PI

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

        if keys[pygame.K_d]:
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
        else:
            self.stamina -= 1 if self.stamina > 0 else 0

        if keys[pygame.K_ESCAPE]:
            print(self.x, self.y, self.angle)
        # проверка на конец уровня

        if 628 < int(self.x) < 690 and 925 < int(self.y) < 977 and self.level == 'paradise':
            self.level = 'space_ship'
            self.game_moment = 'space_ship'
            self.x = 138
            self.y = 138
            self.angle = 0
            self.hp = 0

        if 1800 < int(self.x) < 1876 and 125 < int(self.y) < 176 and self.level == 'space_ship':
            self.game_moment = 'finish'

        if keys[pygame.K_j]:
            self.level = 'space_ship'
            self.game_moment = 'space_ship'

        if keys[pygame.K_k]:
            self.game_moment = 'finish'
        self.angle %= DOUBLE_PI

        if self.hp > 0:
            if time.time() - self.last_resq_time > 2:
                self.hp -= 5
                self.last_resq_time = time.time()

    # контроль мыши

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

    # функция выстрела игрока

    def shoot(self, sprite):
        keys = pygame.key.get_pressed()
        km = pygame.mouse.get_pressed(num_buttons=3)
        if (keys[pygame.K_SPACE] or km[0]) and\
                time.time() - self.last_shoot_time > 0.4 and\
                sprite is not None:
            sprite.affect()
            self.last_shoot_time = time.time()
            return True
        elif (keys[pygame.K_SPACE] or km[0]) and\
                time.time() - self.last_shoot_time > 0.4 and\
                sprite is None:
            self.last_shoot_time = time.time()
            return True
        else:
            return False

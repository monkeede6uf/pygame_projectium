from settings import *
import pygame
import math


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.stamina = 0
        self.regen = False

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        if keys[pygame.K_LSHIFT]:
            if self.stamina <= 190:
                self.stamina += 3
                self.x += player_speed * 2 * cos_a
                self.y += player_speed * 2 * sin_a
            else:
                self.x += player_speed * cos_a
                self.y += player_speed * sin_a
        if not keys[pygame.K_LSHIFT]:
            self.stamina -= 1 if self.stamina > 0 else 0


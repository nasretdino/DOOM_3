from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, screen, world_map, delta_time):
        self.delta_time = delta_time
        self.screen = screen
        self.world_map = world_map
        self.x, self.y = PLAYER_POS
        self.angle = 1 # коэффициент, на который домножается DELTA_ANGLE
        self.get_table_sin()
        self.get_table_cos()


    def get_table_sin(self):
        self.table_sin = {}
        angle = 0
        for i in range(0, int(360 / DELTA_ANGLE)):
            self.table_sin[i] = math.sin(math.radians(angle))
            angle = DELTA_ANGLE * i

    def get_table_cos(self):
        self.table_cos = {}
        angle = 0
        for i in range(0, int(360 / DELTA_ANGLE)):
            self.table_cos[i] = math.cos(math.radians(angle))
            angle = DELTA_ANGLE * i


    def movement(self):
        sin_a = self.table_sin[self.angle]
        cos_a = self.table_cos[self.angle]
        x, y = 0, 0
        speed = PLAYER_SPEED * self.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            x += speed_cos
            y += speed_sin
        if keys[pg.K_s]:
            x -= speed_cos
            y -= speed_sin
        if keys[pg.K_a]:
            x += speed_sin
            y -= speed_cos
        if keys[pg.K_d]:
            x -= speed_sin
            y += speed_cos

        self.check_wall_collision(x, y)

        if keys[pg.K_LEFT]:
            self.angle -= self.delta_time * PLAYER_ROT_SPEED / DELTA_ANGLE
        if keys[pg.K_RIGHT]:
            self.angle += self.delta_time * PLAYER_ROT_SPEED / DELTA_ANGLE

        self.angle = self.in_360(self.angle)


    @staticmethod
    def in_360(angle):
        if round(angle * DELTA_ANGLE, 5) >= 360: angle -= 360 / DELTA_ANGLE
        elif round(angle * DELTA_ANGLE, 5) < 0: angle += 360 / DELTA_ANGLE
        return angle


    def check_wall(self, x, y):
        return (x, y) not in self.world_map

    def check_wall_collision(self, x, y):
        scale = PLAYER_SIZE_SCALE / self.delta_time
        if self.check_wall(int(self.x + x * scale), int(self.y)): self.x += x
        if self.check_wall(int(self.x), int(self.y + y * scale)): self.y += y

    def draw(self):
        pg.draw.circle(self.screen, 'green', (self.x * CELL_PIXELS, self.y * CELL_PIXELS), 15)


    def update(self, delta_time):
        self.delta_time = delta_time
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
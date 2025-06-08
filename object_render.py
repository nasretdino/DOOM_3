import pygame as pg
from settings import *


class ObjectRender:
    def __init__(self, screen):
        self.screen = screen
        self.wall_textures = self.load_wall_textures()

    def draw(self, objects_to_render):
        self.render_game_objects(objects_to_render)

    def render_game_objects(self, objects_to_render):
        list_objects = objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('images/textures/wall_1.png'),
            2: self.get_texture('images/textures/wall_2.png'),
        }
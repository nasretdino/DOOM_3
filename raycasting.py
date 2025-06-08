import pygame as pg

from object_render import ObjectRender
from settings import *
import math


class RayCasting:
    def __init__(self, screen, new_map, player, wall_textures):
        self.screen = screen
        self.map = new_map
        self.player = player
        self.objects_to_render = []
        self.textures = wall_textures


    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            wall_column = self.textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
            )
            wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            self.objects_to_render.append((depth, wall_column, wall_pos))

        return self.objects_to_render

    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.player.pos
        x_map, y_map = self.player.map_pos

        ray_angle = self.player.angle - HALF_FOV / DELTA_ANGLE - 1
        ray_angle = self.player.in_360(ray_angle)

        for ray in range(NUM_RAYS_FOV + 1):
            cos_a = self.player.table_cos[ray_angle] + 1e-6
            sin_a = self.player.table_sin[ray_angle] + 1e-6

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - py) / sin_a
            x_hor = px + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = (int(x_hor), int(y_hor))
                if tile_hor in self.map:
                    texture_hor = self.map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - px) / cos_a
            y_vert = depth_vert * sin_a + py

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.map:
                    texture_vert = self.map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor


            # delete fish
            depth *= self.player.table_cos[self.player.in_360(self.player.angle - ray_angle)]

            proj_height = SCREEN_DIST / (depth + 0.00001)

            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # pg.draw.rect(self.screen, 'white',
            #              (ray * SCALE, (HEIGHT - proj_height) // 2, SCALE, proj_height))

            # pg.draw.line(self.screen, 'yellow', (CELL_PIXELS * px, CELL_PIXELS * py),
            #              (CELL_PIXELS * px + CELL_PIXELS * depth * cos_a, CELL_PIXELS * py + CELL_PIXELS * depth * sin_a), 2)

            ray_angle += 1
            ray_angle = self.player.in_360(ray_angle)

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

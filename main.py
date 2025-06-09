import pygame as pg
from sys import exit
import os

from settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
from weapon import *
from network import*


class Game:
    def __init__(self):
        os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
        os.environ["SDL_WINDOWS_DPI_SCALING"] = "0"
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self.screen)
        self.player = Player(self.screen, self.map.world_map, self.delta_time)
        self.object_render = ObjectRender(self.screen)
        self.raycasting = RayCasting(self.screen, self.map.world_map, self.player, self.object_render.wall_textures)
        self.weapon = Weapon(self.screen, self.object_render.weapon_textures, self.player)

        self.network = Network(self.player,"0.0.0.0" ,"SERVER")

    def update(self):
        self.player.update(self.delta_time)
        self.network.update()
        self.raycasting.update()
        self.player.shoot = self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{int(self.clock.get_fps())}")

    def draw(self):
        self.screen.fill("black")
        self.object_render.draw(self.raycasting.get_objects_to_render())
        self.weapon.draw()
        pg.draw.circle(self.screen, "white", (HALF_WIDTH, HALF_HEIGHT), 2)


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                exit()
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
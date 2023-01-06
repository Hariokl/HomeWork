import pygame as pg
import numpy as np


def init():
    global WIDTH, HEIGHT, TILES_WH, FPS, display, positions, all_sprites, max_i, available_i, enemies_rects
    WIDTH, HEIGHT = 640*1.5, 480*1.5
    TILES_WH = WIDTH // 10 // 2
    FPS = 60
    enemies_rects = list()

    n = 100

    display = pg.display.set_mode((WIDTH, HEIGHT))
    positions = np.full((n, 2), (0., 0.))
    all_sprites = pg.sprite.Group()
    max_i = n
    available_i = [i for i in range(n)]

    map_settings()


def map_settings():
    global map_tiles
    with open("map_1.txt") as map1:
        # троичная системма счистления получилась :D
        translate = {"0": "00", "1": "01", "2": "02", "3": "10", "4": "11"}
        map_tiles = [[translate[x] for x in line.replace("\n", "")] for line in map1.readlines()]

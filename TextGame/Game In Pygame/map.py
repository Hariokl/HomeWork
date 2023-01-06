from enemy import spawn_enemies
import settings as st

import pygame as pg


class Map(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.map_tiles = st.map_tiles
        self.i = st.available_i[0]
        st.available_i.remove(self.i)

        tmap, enemies, player_pos = draw_map(self.map_tiles)

        self.image = tmap
        self.rect = self.image.get_rect()

        st.all_sprites.add(self)
        spawn_enemies(enemies)
        st.positions -= player_pos

    def update(self):
        self.rect.topleft = st.positions[self.i]


def draw_map(tmap):
    map = pg.Surface((len(tmap[0])*st.TILES_WH, len(tmap)*st.TILES_WH))
    twh = st.TILES_WH // 20
    enemies = []
    for j, y in enumerate(tmap):
        for i, x in enumerate(y):
            color = pg.Color((200, 250, 90))
            color1 = pg.Color((150, 200, 90))
            if x == "00":
                color = pg.Color((0, 0, 0))
                color1 = pg.Color((0, 0, 0))
            if x == "02":
                color = pg.Color((250, 200, 90))
                color1 = pg.Color((200, 150, 90))
            if x == "11":
                enemies.append((i, j))
            if x == "10":
                player_pos = i*st.TILES_WH - st.WIDTH // 2 + st.TILES_WH // 2, j*st.TILES_WH - st.HEIGHT // 2 + st.TILES_WH // 2
            pg.draw.rect(map, color, (i*st.TILES_WH, j*st.TILES_WH, st.TILES_WH, st.TILES_WH), 0)
            pg.draw.rect(map, color1, (i*st.TILES_WH+twh, j*st.TILES_WH+twh, st.TILES_WH-twh*2, st.TILES_WH-twh*2), 0)
    return map, enemies, player_pos


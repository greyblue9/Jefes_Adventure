import pygame as pg
import common
import os
from csv import reader


def import_folder(path, file_type):
    file_list = []
    for file in sorted(os.listdir(path)):
        # remove mac's hidden file
        if file == ".DS_Store":
            continue
        full_path = path + "/" + file
        if file_type == "image":
            content = pg.image.load(full_path).convert_alpha()
        elif file_type == "music":
            content = pg.mixer.Sound(full_path)
        elif file_type == "cursor":
            surface = pg.image.load(full_path).convert_alpha()
            content = pg.cursors.Cursor((20, 5), surface)
        file_list.append(content)
    return file_list


def import_sfx(path):
    pg.mixer.set_num_channels(101)
    sfx_list = {}
    for _, __, files in os.walk(path):

        # remove mac's hidden file and sort in order
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        files.sort()

        for index, item in enumerate(files):
            full_path = path + "/" + item
            name = item[:-4]
            sound = pg.mixer.Sound(full_path)

            sfx_list[name] = {"sound": sound, "channel": index + 50}
    return sfx_list


def import_csv(path):
    sprite_map = []
    with open(path) as csv_map:
        level = reader(csv_map, delimiter=",")
        for row in level:
            sprite_map.append(list(map(int, row)))
    return sprite_map


def import_cut_graphic(surface):
    tile_x = int(surface.get_size()[0] / common.TILE_SIZE)
    tile_y = int(surface.get_size()[1] / common.TILE_SIZE)

    cut_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * common.TILE_SIZE
            y = row * common.TILE_SIZE
            new_surface = pg.Surface(
                (common.TILE_SIZE, common.TILE_SIZE), flags=pg.SRCALPHA
            )
            new_surface.blit(
                surface, (0, 0), pg.Rect(x, y, common.TILE_SIZE, common.TILE_SIZE)
            )
            cut_tiles.append(new_surface)
    return cut_tiles

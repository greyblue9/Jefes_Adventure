import pygame as pg
import os
from support import import_folder

pg.init()


class GameImages:
    def __init__(self, path):
        self.dangers = self.get_image_dict(f"{path}/dangers")
        self.decorations = self.get_image_dict(f"{path}/decorations")
        self.enemies = self.get_image_dict(f"{path}/enemies")
        self.food = self.get_image_dict(f"{path}/food")
        self.gates = self.get_image_dict(f"{path}/gates")
        self.ground = self.get_image_dict(f"{path}/ground")
        self.overworld = self.get_image_dict(f"{path}/overworld")
        self.pug = self.get_image_dict(f"{path}/pug")
        self.title = self.get_image_dict(f"{path}/title")
        self.treasure = self.get_image_dict(f"{path}/treasure")
        self.ui = self.get_image_dict(f"{path}/ui")

    def get_image_dict(self, path):
        new_dict = {}
        for item in os.listdir(path):
            full_path = f"{path}/{item}"
            if os.path.isfile(full_path) and item[0] != ".":
                if item[-5].isdigit():
                    return import_folder(path, "image")
                new_dict[item[:-4]] = pg.image.load(full_path).convert_alpha()
            elif os.path.isdir(full_path):
                new_dict[item] = self.get_image_dict(full_path)
        return new_dict

import pygame as pg
import os
from support import import_folder

pg.init()


class GameImages:
    def __init__(self, path):
        self.dangers = self.get_image_dict(path + "/dangers")
        self.decorations = self.get_image_dict(path + "/decorations")
        self.enemies = self.get_image_dict(path + "/enemies")
        self.food = self.get_image_dict(path + "/food")
        self.gates = self.get_image_dict(path + "/gates")
        self.ground = self.get_image_dict(path + "/ground")
        self.overworld = self.get_image_dict(path + "/overworld")
        self.pug = self.get_image_dict(path + "/pug")
        self.title = self.get_image_dict(path + "/title")
        self.treasure = self.get_image_dict(path + "/treasure")
        self.ui = self.get_image_dict(path + "/ui")

    def get_image_dict(self, path):
        new_dict = {}
        for item in os.listdir(path):
            full_path = path + "/" + item
            if os.path.isfile(full_path) and item[0] != ".":
                if item[-5].isdigit():
                    return import_folder(path, "image")
                new_dict[item[:-4]] = pg.image.load(full_path).convert_alpha()
            elif os.path.isdir(full_path):
                new_dict[item] = self.get_image_dict(full_path)
        return new_dict

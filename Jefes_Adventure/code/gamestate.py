import pygame as pg
from abc import abstractmethod, ABC
from common import WIDTH
from support import import_folder


class GameState(ABC, pg.sprite.Sprite):
    def __init__(self, music, **assets):
        super().__init__()
        self.is_over = False

        self.music = music
        if not isinstance(self.music, list):
            self.music.play(loops=-1)
            self.music.set_volume(0.4)

        self.bg = assets["bg"]

        self.buttons = {"name": {"state": None, "obj": None}}

        self.cursors = import_folder("../img/overworld/paws", "cursor")
        self.cursor_index = 1
        self.set_cursor()

    @abstractmethod
    def update(self, event_info):
        for _, button in self.buttons.items():
            if button["obj"]:
                button["obj"].update(event_info)
                if button["obj"].clicked:
                    self.is_over = True

    @abstractmethod
    def next_game_state(self):
        pass

    def set_cursor(self):
        pg.mouse.set_cursor(self.cursors[self.cursor_index])

    @abstractmethod
    def draw(self, display_screen):
        display_screen.blit(self.bg, (0, 0))
        display_screen.blit(self.bg, (WIDTH / 2, 0))

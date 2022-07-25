import pygame as pg
import states as gs
from common import WIDTH, HEIGHT
from ui import SwitchButton
from gamestate import GameState
from settingsmenu import SettingsMenu


class TitleScreen(GameState):
    def __init__(self, music, **assets):
        super().__init__(music, **assets)
        # buttons

        self.imgs = assets["imgs"]

        start_btn = SwitchButton(
            (WIDTH * 2 / 3 - 20, HEIGHT / 2), self.imgs.title["play"], "unlocked"
        )
        setting_btn = SwitchButton(
            (WIDTH * 2 / 3 - 20, HEIGHT / 2 + 130), self.imgs.title["settings"], "unlocked",
        )
        self.buttons = {
            "start": {"state": gs.LevelMenu, "obj": start_btn},
            "settings": {"state": None, "obj": setting_btn},
        }

        # title graphics

        self.flowers = self.imgs.title["fg"]
        self.bar = self.imgs.title["bar"]
        self.pug = self.imgs.title["pug"]
        self.pug_pos = pg.math.Vector2(0, HEIGHT)
        self.pug_speed = 10

        # settings menu sprite
        self.settings = pg.sprite.GroupSingle()
        self.override_state = None

    def update(self, event_info):
        self.pug_speed = (self.pug_speed + 1) % 2
        if self.pug_pos[1] > 0 and self.pug_speed == 0:
            self.pug_pos[1] -= 5

        for state, button in self.buttons.items():
            button["obj"].update(event_info)
            if button["obj"].clicked:
                if state == "start":
                    self.is_over = True
                else:
                    self.settings.add(SettingsMenu(False, imgs=self.imgs))
                    button["obj"].clicked = False

        if self.settings.sprite:
            self.override_state = self.settings.sprite.update(event_info)
        if self.override_state:
            self.is_over = True

    def next_game_state(self):
        self.music.stop()

        if self.override_state:
            if self.override_state is gs.MainGame:
                return self.override_state, (1,1)
            return self.override_state, None

        for _, data in self.buttons.items():
            if data["obj"].clicked:
                return data["state"], None

    def draw(self, display_screen):
        display_screen.blit(self.bg, (0, 0))
        display_screen.blit(self.pug, self.pug_pos)
        display_screen.blit(self.bar, (WIDTH * 2 / 3 + 85, HEIGHT / 2 - 10))
        display_screen.blit(self.flowers, (0, 0))
        for _, data in self.buttons.items():
            data["obj"].draw(display_screen)

        if self.settings.sprite:
            self.settings.sprite.draw(display_screen)

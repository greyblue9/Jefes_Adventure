import pygame as pg
from support import import_sfx

pg.mixer.init()


class SFXManager:
    def __init__(self):
        self.sounds = import_sfx("../audio/effects")

    def play_sfx(self, sound_key: str):
        sound = self.sounds[sound_key]["sound"]
        channel = self.sounds[sound_key]["channel"]
        pg.mixer.Channel(channel).play(sound)

    def close_all(self):
        for sound in self.sounds.values():
            if pg.mixer.Channel(sound["channel"]).get_busy():
                pg.mixer.Channel(sound["channel"]).stop()
        pg.mixer.quit()

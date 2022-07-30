import pygame as pg
import states as gs
import json
from common import WIDTH, HEIGHT
from ui import SwitchButton, ToggleButton


class SettingsMenu(pg.sprite.Sprite):
    def __init__(self, in_game, **assets):
        super().__init__()
        self.imgs = assets["imgs"]
        self.in_game = in_game
        with open('../assets/settings.json', 'r') as f:
            self.settings_data = json.load(f)

        if in_game:
            self.image = self.imgs.ui["table_big"]
        else:
            self.image = self.imgs.ui["table_small"]
        self.rect = self.image.get_rect(center= (WIDTH/2, HEIGHT/2))

        self.set_buttons()

        font = pg.font.Font("../assets/settings.otf", 30)
        jfont = pg.font.Font("../assets/jsettings.ttf", 32)
        jfont2 = pg.font.Font("../assets/jsettings.ttf", 25)
        self.font = {0: font, 1: jfont}
        self.font2 = {0: font, 1: jfont2}
        self.color = (33, 131, 71)

        text_rects = [
            self.rect.topleft + pg.math.Vector2(175,105),
            self.rect.topleft + pg.math.Vector2(175,170),
            self.rect.topleft + pg.math.Vector2(175,235),
            self.rect.topleft + pg.math.Vector2(115,380),
            self.rect.topleft + pg.math.Vector2(115,460),
            self.rect.topleft + pg.math.Vector2(305,380),
            self.rect.topleft + pg.math.Vector2(305,460),
            ]
        jtext_rects = [
            self.rect.topleft + pg.math.Vector2(175,114),
            self.rect.topleft + pg.math.Vector2(175,179),
            self.rect.topleft + pg.math.Vector2(175,244),
            self.rect.topleft + pg.math.Vector2(115,394),
            self.rect.topleft + pg.math.Vector2(115,474),
            self.rect.topleft + pg.math.Vector2(305,394),
            self.rect.topleft + pg.math.Vector2(305,474),
            ]
        self.text_rects = {0: text_rects,1: jtext_rects}

    def set_buttons(self):
        close_btn = SwitchButton(
            self.rect.topleft + pg.math.Vector2(10,10), self.imgs.ui["buttons"]["close"]
        )
        music_btn = ToggleButton(
            self.rect.topleft + pg.math.Vector2(110,105), self.imgs.ui["buttons"]["music"], self.settings_data["music"]
        )
        sfx_btn = ToggleButton(
            self.rect.topleft + pg.math.Vector2(110,170), self.imgs.ui["buttons"]["sound"], self.settings_data["sound"]
        )
        language_btn = ToggleButton(
            self.rect.topleft + pg.math.Vector2(110,235), self.imgs.ui["buttons"]["language"], self.settings_data["language"]
        )
        self.buttons = {
            "close": {"state": None, "obj": close_btn},
            "music": {"state": None, "obj": music_btn},
            "sound": {"state": None, "obj": sfx_btn},
            "language": {"state": None, "obj": language_btn},
        }

        if self.in_game:
            menu_btn = SwitchButton(
                self.rect.topleft + pg.math.Vector2(50,380), self.imgs.ui["buttons"]["menu"],
            )
            back_btn = SwitchButton(
                self.rect.topleft + pg.math.Vector2(50,460), self.imgs.ui["buttons"]["back"],
            )
            home_btn = SwitchButton(
                self.rect.topleft + pg.math.Vector2(240,380), self.imgs.ui["buttons"]["home"],
            )
            restart_btn = SwitchButton(
                self.rect.topleft + pg.math.Vector2(240,460), self.imgs.ui["buttons"]["restart"],
            )
            extra_buttons = {
                "menu": {"state": gs.LevelMenu, "obj": menu_btn},
                "back": {"state": None, "obj": back_btn},
                "home": {"state": gs.TitleScreen, "obj": home_btn},
                "restart": {"state": gs.MainGame, "obj": restart_btn},
            }
            self.buttons.update(extra_buttons)

    def check_buttons(self):
        for name, button in self.buttons.items():
            if button["obj"].clicked:
                button["obj"].clicked = False
                return name

    def update_json(self, value):
        self.settings_data[value] = abs(self.settings_data[value] - 1)
        with open("../assets/settings.json", "w") as f:
            json.dump(self.settings_data, f)

    def update(self, event_info):
        for _, button in self.buttons.items():
            if button["obj"]:
                button["obj"].update(event_info)

        clicked_button = self.check_buttons()
        state = None
        if clicked_button in ["back", "close", "restart", "menu", "home"]:
            if clicked_button in ["restart", "menu", "home"]:
                state = self.buttons[clicked_button]["state"]
            self.kill()
            return state
        elif clicked_button in ["music", "sound", "language"]:
            self.update_json(clicked_button)
            self.buttons[clicked_button]["obj"].switch()


    def draw(self, display_screen):
        # display table
        display_screen.blit(self.image, self.rect)

        # process settings items in English or Japanese
        language = self.settings_data["language"]
        text_contents = {
            0: ["MUSIC", "SOUND FX", "LANGUAGE", "MENU", "BACK", "HOME", "RESTART"], 
            1:["BGM", "ｻｳﾝﾄﾞｴﾌｪｸﾄ", "言語", "ﾚﾍﾞﾙ選択", "バック", "ﾒｲﾝへ戻る", "リトライ"],
            }
        font = self.font[language]
        font2 = self.font2[language]

        # display text
        text = [
            font.render(text_contents[language][0], True, self.color),
            font.render(text_contents[language][1], True, self.color),
            font.render(text_contents[language][2], True, self.color),
            ]
        if self.in_game:
            text.extend([
                font2.render(text_contents[language][3], True, self.color),
                font2.render(text_contents[language][4], True, self.color),
                font2.render(text_contents[language][5], True, self.color),
                font2.render(text_contents[language][6], True, self.color),
                ])
        for item in zip(text, self.text_rects[language]):
            display_screen.blit(item[0], item[1])

        # display buttons
        for _, button in self.buttons.items():
            button["obj"].draw(display_screen)
        

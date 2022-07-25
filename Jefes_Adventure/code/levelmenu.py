import pygame as pg
import states as gs
import json
from common import WIDTH, HEIGHT
from ui import SwitchButton, AnimatedButton
from gamestate import GameState
from player import NPC


class LevelMenu(GameState):
    def __init__(self, music, **assets):
        super().__init__(music, **assets)

        # stages and levels
        with open("../assets/save.json", "r") as f:
            save_data = json.load(f)
        self.max_stage = save_data["max_stage"]
        self.max_level = save_data["max_level"]
        self.current_level = 1
        self.current_stage = 1

        # movement logic
        self.stage_set = False
        self.moving = False

        # buttons and pointers
        self.imgs = assets["imgs"]
        self.setup_buttons()
        pg.mouse.set_pos(self.stage_buttons[1].rect.center)
        self.sun = self.imgs.overworld["sun"]
        self.sun_spot = pg.math.Vector2(-200, -200)

        # decorative animation
        self.player_sprite = pg.sprite.GroupSingle(
            NPC(pg.math.Vector2(WIDTH / 6 + 100, HEIGHT * 2 / 3), self.imgs.pug["run"])
        )

        # time
        self.start_time = pg.time.get_ticks()
        self.allow_input = False
        self.pause_length = 500

    def setup_buttons(self):
        self.stage_buttons = []
        self.stage_states = []

        with open("../assets/stages.json", "r") as f:
            stages = json.load(f)
        with open("../assets/levels.json", "r") as f:
            levels = json.load(f)

        for index, data in enumerate(stages.values()):
            available = "un" * (index - 1 <= self.max_stage) + "locked"
            button = AnimatedButton(
                data["node_pos"],
                self.imgs.overworld["stage"][data["graphics"]],
                available,
            )
            self.stage_buttons.append(button)
            if index == 1:
                self.stage_states.append(gs.TitleScreen)
            else:
                self.stage_states.append(data["graphics"])

        self.level_buttons = []
        self.level_states = []
        for index, data in enumerate(levels.values()):
            available = "un" * (index <= self.max_level) + "locked"
            button = SwitchButton(
                data["node_pos"],
                self.imgs.overworld["levels"][data["graphics"]],
                "unlocked",
            )
            self.level_buttons.append(button)
            if index == 0:
                self.level_states.append(0)
            else:
                self.level_states.append(gs.MainGame)

    def level_button_availability(self):
        for level, button in enumerate(self.level_buttons):
            if self.current_stage < self.max_stage + 1 or level <= self.max_level:
                button.state = "unlocked"
            else:
                button.state = "locked"

    def check_button_clicked(self, node_set):
        for index, button in enumerate(node_set):
            if button.clicked:
                button.clicked = False
                return index

    def input_mouse(self, event_info):
        for event in event_info["events"]:
            if event.type == pg.MOUSEBUTTONUP:
                self.moving = False

        if self.stage_set:
            mousex, mousey = event_info["mouse pos"]
            if mousey < HEIGHT * 2 / 3:
                pg.mouse.set_pos(mousex, HEIGHT * 2 / 3)

        if self.moving or not self.allow_input:
            return

        s = self.check_button_clicked(self.stage_buttons)
        l = self.check_button_clicked(self.level_buttons)
        self.moving = True

        if s != None:
            if not self.stage_set:
                if type(self.stage_states[s]) == str:
                    pg.mouse.set_pos(self.level_buttons[1].rect.center)
                    self.current_stage = int(self.stage_states[s]) + 1
                    self.stage_set = True
                    self.sun_spot = self.stage_buttons[
                        s
                    ].rect.topleft - pg.math.Vector2(0, 50)
                else:
                    self.stage_buttons[s].clicked = True
                    self.is_over = True
        elif l != None:
            if l == 0:
                self.stage_set = False
                pg.mouse.set_pos(self.stage_buttons[self.current_stage].rect.center)
                self.current_stage = 1
                self.sun_spot = pg.math.Vector2(-200, -200)
            else:
                self.current_level = l
                self.level_buttons[l].clicked = True
                self.is_over = True

    def next_game_state(self):
        self.music.stop()

        def get_clicked(buttons):
            return [i for i, button in enumerate(buttons) if button.clicked]

        if self.stage_set:
            level_info = (self.current_stage - 1, self.current_level)
            return self.level_states[get_clicked(self.level_buttons)[0]], level_info
        else:
            return (self.stage_states[get_clicked(self.stage_buttons)[0]], None)

    def input_timer(self):
        if not self.allow_input:
            current_time = pg.time.get_ticks()
            if current_time - self.start_time >= self.pause_length:
                self.allow_input = True

    def update(self, event_info):
        super().update(event_info)
        self.level_button_availability()
        for button in self.stage_buttons:
            button.update(event_info)
        for button in self.level_buttons:
            button.update(event_info)

        self.input_timer()
        self.input_mouse(event_info)

        hover_index = [i for i, button in enumerate(self.stage_buttons) if button.hover]
        if hover_index and not self.stage_set:
            self.cursor_index = hover_index[0]
            self.set_cursor()

    def draw(self, display_screen):
        super().draw(display_screen)
        self.player_sprite.update()
        self.player_sprite.draw(display_screen)

        display_screen.blit(self.sun, self.sun_spot)

        for button in self.stage_buttons:
            button.draw(display_screen)
        if self.stage_set:
            for button in self.level_buttons:
                button.draw(display_screen)

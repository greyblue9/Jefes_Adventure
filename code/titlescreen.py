import pygame as pg
import states as gs
from settings import WIDTH, HEIGHT
from ui import SwitchButton
from gamestate import GameState
from support import import_folder

class TitleScreen(GameState):
	def __init__(self, music, **assets):
		super().__init__(music, **assets)
		# buttons
		start_btn = SwitchButton((WIDTH*2/3-20,HEIGHT/2),"../img/title/play","PLAY","unlocked")
		setting_btn = SwitchButton((WIDTH*2/3-20,HEIGHT/2+130),"../img/title/settings","SETTINGS","unlocked")
		self.buttons = [start_btn, setting_btn]
		self.states = [gs.LevelMenu, gs.SettingsMenu] #change to setting game state

		# title graphics
		self.flowers = pg.image.load('../img/title/fg.png').convert_alpha()
		self.bar = pg.image.load('../img/title/bar.png').convert_alpha()
		self.pug = pg.image.load('../img/title/pug.png').convert_alpha()
		self.pug_pos = pg.math.Vector2(0,HEIGHT)
		self.pug_speed = 10

	def update(self, event_info):
		super().update(event_info)
		self.pug_speed = (self.pug_speed + 1) % 2
		if self.pug_pos[1] > 0 and self.pug_speed == 0:
			self.pug_pos[1] -= 5

	def next_game_state(self):
		self.music.stop()
		clicked_index = [i for i,button in enumerate(self.buttons) if button.clicked]
		return (self.states[clicked_index[0]],None)

	def draw(self, display_screen):
		display_screen.blit(self.bg, (0,0))
		display_screen.blit(self.pug, self.pug_pos)
		display_screen.blit(self.bar, (WIDTH*2/3+85,HEIGHT/2-10))
		display_screen.blit(self.flowers, (0,0))
		for button in self.buttons:
			button.draw(display_screen)

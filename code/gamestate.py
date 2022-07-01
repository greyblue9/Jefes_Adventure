import pygame as pg
from abc import abstractmethod, ABC
from settings import WIDTH
from support import import_cursors

class GameState(ABC, pg.sprite.Sprite):
	def __init__(self, music, **assets):
		super().__init__()
		self.is_over = False

		self.music = music
		if type(self.music) != list:
			self.music.play(loops = -1)
			self.music.set_volume(0.4)

		self.bg = assets["bg"]

		self.buttons = []

		self.cursors = import_cursors('../img/overworld/paws')
		self.cursor_index = 1
		self.set_cursor()

	@abstractmethod
	def update(self, event_info):
		for button in self.buttons:
			button.update(event_info)
			if button.clicked:
				self.is_over = True

	@abstractmethod
	def next_game_state(self):
		pass

	def set_cursor(self):
		pg.mouse.set_cursor(self.cursors[self.cursor_index])

	@abstractmethod
	def draw(self, display_screen):
		display_screen.blit(self.bg, (0,0))
		display_screen.blit(self.bg, (WIDTH/2,0))

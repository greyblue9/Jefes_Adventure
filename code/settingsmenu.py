import pygame as pg
import states as gs
from settings import WIDTH, HEIGHT
from ui import SwitchButton, AnimatedButton
from gamestate import GameState
from support import import_folder

class SettingsMenu(GameState):
	def __init__(self, sound, **images):
		super().__init__(sound, **images)

	def next_game_state(self):
		pass

	def update(self, event_info):
		super().update(event_info)

	def draw(self, display_screen):
		display_screen.fill((120,120,120))
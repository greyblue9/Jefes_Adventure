import pygame as pg
import states as gs
from settings import WIDTH, HEIGHT
from ui import SwitchButton, AnimatedButton
from gamestate import GameState
from game_data import stages, levels
from support import import_folder
from player import UPC

class LevelMenu(GameState):
	def __init__(self, music, **assets):
		super().__init__(music, **assets)

		# stages and levels
		self.max_stage = 4
		self.max_level = 7
		self.current_level = 1
		self.current_stage = 1
		
		# movement logic
		self.stage_set = False
		self.moving = False

		# buttons and pointers
		self.setup_buttons()
		pg.mouse.set_pos(self.stage_buttons[1].rect.center)
		self.sun = pg.image.load('../img/overworld/sun.png').convert_alpha()
		self.sun_spot = pg.math.Vector2(-200,-200)

		# decorative animation
		self.player_sprite = pg.sprite.GroupSingle(UPC(pg.math.Vector2(WIDTH/6 + 100,HEIGHT*2/3)))

		# time
		self.start_time = pg.time.get_ticks()
		self.allow_input = False
		self.pause_length = 500

	def setup_buttons(self):
		self.stage_buttons = []
		self.stage_states = []
		for index, data in enumerate(stages.values()):
			available = 'un' * (index - 1 <= self.max_stage) + 'locked'
			button = AnimatedButton(data['node_pos'],data['graphics'],data['content'],available)
			self.stage_buttons.append(button)
			if index == 1:
				self.stage_states.append(gs.TitleScreen)
			else:
				self.stage_states.append(data['content'])

		self.level_buttons = []
		self.level_states = []
		for index, data in enumerate(levels.values()):
			available = 'un' * (index <= self.max_level) + 'locked'
			button = SwitchButton(data['node_pos'],data['graphics'],data['content'],available)
			self.level_buttons.append(button)
			if index == 0:
				self.level_states.append(0)
			else:
				self.level_states.append(gs.MainGame)

	def check_button_clicked(self, node_set):
		for index,button in enumerate(node_set):
			if button.clicked:
				button.clicked = False
				return index

	def input_mouse(self, event_info):
		for event in event_info["events"]:
			if event.type == pg.MOUSEBUTTONUP:
				self.moving = False

		if self.moving or not self.allow_input: return

		s = self.check_button_clicked(self.stage_buttons)
		l = self.check_button_clicked(self.level_buttons)
		self.moving = True

		if s != None:
			if not self.stage_set:
				if type(self.stage_states[s]) == str:
					pg.mouse.set_pos(self.level_buttons[1].rect.center)
					self.current_stage = int(self.stage_states[s]) + 1
					self.stage_set = True
					self.sun_spot = self.stage_buttons[s].rect.topleft - pg.math.Vector2(0,50)
				else:
					self.stage_buttons[s].clicked = True
					self.is_over = True
		elif l != None:
			if l == 0:
				self.stage_set = False
				pg.mouse.set_pos(self.stage_buttons[self.current_stage].rect.center)
				self.current_stage = 1
				self.sun_spot = pg.math.Vector2(-200,-200)
			else:
				self.current_level = l
				self.level_buttons[l].clicked = True
				self.is_over = True

	""" Keyboard Input (not using)
	def input(self, event_info):
		keys = event_info["keys"]
		
		for event in event_info["events"]:
			if event.type == pg.KEYUP:
				self.moving = False

		if not self.moving:
			if self.stage_set:
				if keys[pg.K_RIGHT] and self.current_level < self.max_level:
					self.current_level += 1
					self.moving = True
				elif keys[pg.K_LEFT] and self.current_level > 0:
					self.current_level -= 1
					self.moving = True
				elif keys[pg.K_SPACE]:
					if self.current_level == 0:
						self.moving = True
						self.stage_set = False
						self.current_level = 1
					else: 
						# play current_stage - 1 : current_level
			else:
				if keys[pg.K_RIGHT] and self.current_stage - 1 < self.max_stage: #index offset to match level positions
					self.current_stage += 1
					self.moving = True
				elif keys[pg.K_LEFT] and self.current_stage > 1:
					self.current_stage -= 1
					self.moving = True
				elif keys[pg.K_DOWN] and self.current_stage != 0:
					self.current_stage = 0
					self.moving = True
				elif keys[pg.K_UP] and self.current_stage == 0:
					self.current_stage = 1
					self.moving = True
				elif keys[pg.K_SPACE]:
						if self.current_stage == 1:
							self.buttons[0].clicked = True
						else:
							self.stage_set = True
							self.moving = True
	"""

	def next_game_state(self):
		self.music.stop()
		if self.stage_set:
			clicked_index = [i for i,button in enumerate(self.level_buttons) if button.clicked]
			level_info = (self.current_stage - 1,self.current_level)
			return (self.level_states[clicked_index[0]],level_info)
		else:
			clicked_index = [i for i,button in enumerate(self.stage_buttons) if button.clicked]
			return (self.stage_states[clicked_index[0]],None)

	def input_timer(self):
		if not self.allow_input:
			current_time = pg.time.get_ticks()
			if current_time - self.start_time >= self.pause_length:
				self.allow_input = True

	def update(self, event_info):
		super().update(event_info)
		
		for button in self.stage_buttons:
			button.update(event_info)
		for button in self.level_buttons:
			button.update(event_info)

		self.input_timer()
		self.input_mouse(event_info)

		hover_index = [i for i,button in enumerate(self.stage_buttons) if button.hover]
		if len(hover_index) and not self.stage_set:
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

import pygame as pg
from settings import TILE_SIZE
from support import import_folder
from player import Player
from particles import BoneGetEffect

class Tile(pg.sprite.Sprite):
	def __init__(self,pos,size):
		super().__init__()
		self.image = pg.Surface((size,size))
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		#shift with the world
		self.rect.x += x_shift

class Goal(Tile): # invisible indicator for player to collide with goal
	def __init__(self,pos,size):
		super().__init__(pos,size)
		self.rect.y -= TILE_SIZE

class AnimatedTile(Tile): #tiles with animation
	def __init__(self, pos, size, path):
		super().__init__(pos, size)
		self.frames = import_folder(path, 'image')
		self.frame_index = 0
		self.frame_speed = 0.02
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
	
	def animate(self):
		self.frame_index = (self.frame_index + self.frame_speed) % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

class BoneTile(AnimatedTile): # bones
	def __init__(self, pos, size, path, gulp):
		super().__init__(pos,size,path)
		self.frame_speed = 0.05
		#load sounds
		self.gulp_sound = gulp
		self.gulp_sound.set_volume(1.0)

	def __del__(self):
		#play swallow sound when bone disappears
		self.gulp_sound.play(loops = 0)

class TrapTile(AnimatedTile): # dangers
	def __init__(self, pos, size, path):
		super().__init__(pos,size,path)
		self.frame_speed = 0.07

class ValueChangeTile(AnimatedTile): # tiles that change when condition is met
	def __init__(self, pos, size, path, player):
		super().__init__(pos,size,path)
		self.frame_speed = 0
		self.is_open = False
		self.player = player

	def conditions(self):
		#none yet
		pass

	def check_open(self):
		if self.is_open:
			self.image = self.frames[1]

	def update(self,x_shift):
		self.conditions()
		self.check_open()
		self.rect.x += x_shift

class TreasureTile(ValueChangeTile): # treasures
	def __init__(self,pos,size,path,player):
		super().__init__(pos,size,path,player)
		self.particle = pg.sprite.GroupSingle()
		self.pos = pos
		self.done = False

	def conditions(self):
		if abs(self.rect.x - self.player.rect.x) < TILE_SIZE and self.player.digging and self.done == False:
			self.is_open = True
			self.particle.add(BoneGetEffect(self.pos, self.player))
			self.done = True

	def update(self, x_shift, display_surface):
		super().update(x_shift)
		self.particle.update(x_shift)
		# flicker image
		if self.particle and round(self.particle.sprite.index,3)%4:
			self.particle.draw(display_surface)

class ExitTile(ValueChangeTile): # exit
	def __init__(self, pos, size, path, player):
		super().__init__(pos,size,path, player)
		self.rect = self.image.get_rect(midleft = pos)

	def conditions(self):
		if self.player.bones == 10:
			self.is_open = True

class StaticTile(Tile): # ground
	def __init__(self,pos,size,surface):
		super().__init__(pos,size)
		self.image = surface

class FloatingTile(StaticTile): # platforms
	def __init__(self,pos,size,surface):
		super().__init__(pos,size,surface)
		self.rect = self.image.get_rect(topleft = pos)
		self.rect.h -= 0.5 * TILE_SIZE

class InvisibleTile(StaticTile): # entrance gate
	def __init__(self, pos, size, path):
		super().__init__(pos,size,path)
		self.rect = self.image.get_rect(midleft = pos)

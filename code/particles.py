import pygame as pg
from support import import_folder

class ParticleEffect(pg.sprite.Sprite):
	def __init__(self,pos,type,player = None):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5

		if type == 'explosion': 
			subfolder = 'enemies/'
		else: 
			subfolder = 'pug/dust_particles/'
		self.frames = import_folder('../img/' + subfolder + type, 'image')
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.player = player

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
			if self.player: 
				self.player.digging = False
				self.player.barking = False
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

class BoneGetEffect(pg.sprite.Sprite):
	def __init__(self,pos, player):
		super().__init__()
		self.image = pg.image.load('../img/food/burried_bone.png').convert_alpha()

		self.rect = self.image.get_rect(center= pos + pg.math.Vector2(32,20))
		self.animation_speed = 0.5
		self.index = 0.0
		self.killtime = 100
		self.pos = pos
		self.player = player
		self.counted = False

	def animate(self):
		#float up
		self.rect.move_ip((0,-2))

	def update(self, x_shift):
		self.rect.x += x_shift
		self.index += self.animation_speed
		if round(self.index,3).is_integer():
			if self.index < 50:
				self.animate()
				if not self.counted:
					self.player.bones += 1
					self.counted = True
		if self.index > self.killtime:
			self.kill()
			

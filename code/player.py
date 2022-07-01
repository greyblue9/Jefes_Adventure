import pygame as pg
from pygame.locals import *
from support import import_folder
from settings import WIDTH
from math import sin

class UPC(pg.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.3
		if type(self.animations) == list:
			self.image = self.animations[self.frame_index]
			self.rect = self.image.get_rect(topleft = pos)

		self.direction = pg.math.Vector2(1,0)
		self.speed = 1
		self.facing_right = True

	def import_character_assets(self):
		character_path = '../img/pug/run'
		self.animations = import_folder(character_path, 'image')

	def animate(self):
		if self.rect.x >= WIDTH*5/6:
			self.facing_right = False
			self.direction.x = -1
		if self.rect.x <= WIDTH/6:
			self.facing_right = True
			self.direction.x = 1

		self.rect.x += self.direction.x * self.speed

		self.frame_index = (self.frame_index + self.animation_speed) % len(self.animations)
		image = self.animations[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			self.image = pg.transform.flip(image,True,False)

	def update(self):
		#run back and forth
		self.animate()
		
class Player(UPC):
	def __init__(self,pos,create_action_sprite, sfx):
		super().__init__(pos)
		self.import_character_assets()
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)

		# audio
		self.bark_sound = sfx[0]
		self.dig_sound = sfx[1]
		self.jump_sound = sfx[3]
		self.ouch_sound = sfx[4]
		
		# dust particles 
		self.dust_run_particles = import_folder('../img/pug/dust_particles/run', 'image')
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.create_action_sprite = create_action_sprite

		# player movement
		self.speed = 4
		self.gravity = 0.5
		self.jump_speed = -14
		self.hit_rect = pg.Rect(self.rect.topleft - pg.math.Vector2(5,5), (self.rect.width - 10, self.rect.height - 10))

		# player state
		self.state = 'idle'
		self.digging = False
		self.barking = False
		self.on_ground = False

		# player items
		self.bones = 0

		# damage management
		self.guard = False
		self.guard_length = 1000
		self.hurt_time = 0

	def import_character_assets(self):
		character_path = '../img/pug/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'bark':[],'dig':[]}
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path, 'image')

	def get_input(self):
		keys = pg.key.get_pressed()

		#left and right movement
		if keys[K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		#jump movement
		if keys[K_SPACE] and self.on_ground:
			self.jump()
			self.create_action_sprite(self.rect.midbottom, "jump")

		#bark movement
		if keys[K_UP] and self.on_ground:
			self.bark()
			self.create_action_sprite(self.rect.midtop, "bark")

		#dig movement
		if keys[K_DOWN] and self.on_ground:
			self.dig()
			self.create_action_sprite(self.rect.midbottom, "dig")

	def animate(self):
		animation = self.animations[self.state]

		# loop over frame index 
		self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.hit_rect.bottomleft
		else:
			self.image = pg.transform.flip(image,True,False)
			self.rect.bottomright = self.hit_rect.bottomright

		if self.guard:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

	def run_dust_animation(self, display_surface):
		if self.state == 'run' and self.on_ground:
			self.dust_frame_index = (self.dust_frame_index + self.dust_animation_speed) % len(self.dust_run_particles)
			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pg.math.Vector2(6,10)
				display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pg.math.Vector2(6,10)
				flipped_dust_particle = pg.transform.flip(dust_particle,True,False)
				display_surface.blit(flipped_dust_particle,pos)

	def get_state(self):
		if self.direction.y < 0:
			self.state = 'jump'
		elif self.direction.y > 1:
			self.state = 'fall'
		else:
			if self.direction.x != 0:
				self.state = 'run'
			else:
				if self.digging:
					self.state = 'dig'
				elif self.barking:
					self.state = 'bark'
				else:
					self.state = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.hit_rect.y += self.direction.y

	def jump(self):
		#run with SPACE key
		self.direction.y = self.jump_speed
		if self.jump_sound.get_num_channels() < 1:
			self.jump_sound.play(loops = 0)
		print(self.jump_sound.get_num_channels())

	def bark(self):
		#run with UP key
		self.barking = True
		if self.bark_sound.get_num_channels() < 1:
			self.bark_sound.play(loops = 0)
		print(self.bark_sound.get_num_channels())

	def dig(self):
		#run with DOWN key
		self.digging = True
		if self.dig_sound.get_num_channels() < 1:
			self.dig_sound.play(loops = 0)
		print(self.dig_sound.get_num_channels())

	def get_damage(self):
		if not self.guard:
			self.ouch_sound.play(loops = 0)
			self.guard = True
			self.hurt_time = pg.time.get_ticks()
			return -10

	def guard_timer(self):
		if self.guard:
			current_time = pg.time.get_ticks()
			if current_time - self.hurt_time >= self.guard_length:
				self.guard = False

	def wave_value(self):
		val = sin(pg.time.get_ticks())
		if val >= 0: return 255
		return 0

	def update(self, display_surface):
		self.get_input()
		self.get_state()
		self.animate()
		self.run_dust_animation(display_surface)
		self.guard_timer()
		self.wave_value()		

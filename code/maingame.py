import pygame as pg
import states as gs
from settings import WIDTH, HEIGHT, TILE_SIZE
from support import import_csv, import_cut_graphic
from ui import SwitchButton, Bar, BoneIndicator
from gamestate import GameState
from player import Player
from tiles import *
from enemy import Enemy
from particles import ParticleEffect
from game_data import game_levels, stages

class MainGame(GameState):
	def __init__(self, level_code, music, **assets):
		
		# level setup
		super().__init__(music, **assets)
		self.stage, self.level = level_code
		self.stage = max(0,self.stage)
		self.music[self.stage].play(loops = -1)
		self.music[self.stage].set_volume(0.4)
		
		# game-over variables
		self.new_max_level = stages[self.stage]['unlock']
		self.completed = False

		# movement help
		self.world_shift = 0

		# player initialization
		self.player = pg.sprite.GroupSingle()
		self.goal = pg.sprite.GroupSingle()
		# ※ player and goal are set up in the Gates Setup ※
		self.current_health = 100
		self.sfx = assets["sfx"]

		# dust
		self.particle_sprite = pg.sprite.GroupSingle()
		self.player_on_ground = False
		self.enemy_dust = pg.sprite.Group()

		# setup tile sprites
		self.setup_sprites()

		# setup UI indicators
		self.health_bar = Bar((5,5), '../img/ui/bars/health')
		self.bone_bar = BoneIndicator((42,42), '../img/ui/bars/bones')

		# setup buttons
		back_to_level = SwitchButton((500,0), '../img/ui/buttons/back', 'BACK', 'unlocked')
		back_to_home = SwitchButton((600,0), '../img/ui/buttons/home', 'HOME', 'unlocked')
		self.buttons = [back_to_level, back_to_home]
		self.states = [gs.LevelMenu, gs.TitleScreen]

	def create_tilegroup(self,layout,type):
		sprite_group = pg.sprite.Group()
		for row_index, row in enumerate(layout):
			for col_index, value in enumerate(row):
				if value != "-1":
					x,y = [col_index * TILE_SIZE, row_index * TILE_SIZE]

					if type == "ground":
						ground_tiles = import_cut_graphic("../img/ground/ground.png")
						tile_surface = ground_tiles[int(value)]
						if int(value) < 2: sprite = FloatingTile((x,y),TILE_SIZE, tile_surface)
						else: sprite = StaticTile((x,y),TILE_SIZE, tile_surface)

					elif type == "decorations":
						deco_type = {"0":"bush","1":"grass","2":"mushroom"}
						sprite = AnimatedTile((x,y),TILE_SIZE, "../img/decorations/" + deco_type[value])

					elif type == "danger":
						deco_type = {"0":"cactus","1":"water","2":"spikes"}
						sprite = TrapTile((x,y),TILE_SIZE, "../img/dangers/" + deco_type[value])

					elif type == "bones":
						sprite = BoneTile((x,y),TILE_SIZE, "../img/food/bones", self.sfx[2])

					elif type == "enemies":
						deco_type = {"0":"bee","2":"frog","3":"mouse","4":"snail","5":"worm"}
						sprite = Enemy((x,y),TILE_SIZE,deco_type[value])

					elif type == "constraints":
						sprite = Tile((x,y),TILE_SIZE)

					elif type == "gates":
						if value == "1":
							# Create goal at exit gate
							sprite = ExitTile((x,y),TILE_SIZE,"../img/gates/exit", self.player.sprite)
							self.goal.add(sprite)
							continue
						else:
							image = pg.image.load("../img/gates/start.png").convert_alpha()
							sprite = InvisibleTile((x,y),TILE_SIZE,image)

							# Create player at start gate
							player_sprite = Player((x + TILE_SIZE/2, y - TILE_SIZE/2), self.create_action_sprite, self.sfx)
							self.player.add(player_sprite)

					elif type == "treasures":
						path = "../img/treasure"
						sprite = TreasureTile((x,y),TILE_SIZE, path, self.player.sprite)

					sprite_group.add(sprite)
		return sprite_group

	def setup_sprites(self):
		level_data = game_levels[self.stage][self.level]
		# ground setup
		ground_layout = import_csv(level_data["ground"])
		self.ground_sprites = self.create_tilegroup(ground_layout,"ground")
		# decoration setup
		decoration_layout = import_csv(level_data["decorations"])
		self.decoration_sprites = self.create_tilegroup(decoration_layout,"decorations")
		# bones setup
		bones_layout = import_csv(level_data["bones"])
		self.bone_sprites = self.create_tilegroup(bones_layout,"bones")
		# dangers setup
		dangers_layout = import_csv(level_data["danger"])
		self.danger_sprites = self.create_tilegroup(dangers_layout,"danger")
		# gates setup
		gates_layout = import_csv(level_data["gates"])
		self.gate_sprites = self.create_tilegroup(gates_layout,"gates")
		# treasures setup
		treasures_layout = import_csv(level_data["treasures"])
		self.treasure_sprites = self.create_tilegroup(treasures_layout,"treasures")
		# enemies setup
		enemy_layout = import_csv(level_data["enemies"])
		self.enemy_sprites = self.create_tilegroup(enemy_layout, "enemies")
		# enemy constraing setup
		constraint_layout = import_csv(level_data["constraints"])
		self.constraint_sprites = self.create_tilegroup(constraint_layout,"constraints")

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < WIDTH / 4 and direction_x < 0: #Left side of the screen
			self.world_shift = 5
			player.speed = 0
		elif player_x > 3 * WIDTH / 4 and direction_x > 0: #Right side of the screen
			self.world_shift = -5
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 5

	def create_action_sprite(self,pos,type):
		if type == "jump":
			v = pg.math.Vector2(10,5)
		elif type == "bark":
			v = pg.math.Vector2(-35,12)
		else: #type == "dig"
			v = pg.math.Vector2(-20,5)

		if self.player.sprite.facing_right:
			pos -= v
		else:
			v.y *= -1
			pos += v

		particle_sprite = ParticleEffect(pos,type,self.player.sprite)
		self.particle_sprite.add(particle_sprite)

	def get_player_on_ground(self):
		# determine if player is on ground before action
		self.player_on_ground = self.player.sprite.on_ground

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground:
			if self.player.sprite.facing_right:
				offset = pg.math.Vector2(10,15)
			else:
				offset = pg.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.particle_sprite.add(fall_dust_particle)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.hit_rect.x += player.direction.x * player.speed

		for sprite in self.ground_sprites.sprites():
			if sprite.rect.colliderect(player.hit_rect):
				if player.direction.x < 0: 
					player.hit_rect.left = sprite.rect.right
				elif player.direction.x > 0:
					player.hit_rect.right = sprite.rect.left

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.ground_sprites.sprites() + self.treasure_sprites.sprites():
			if sprite.rect.colliderect(player.hit_rect):
				if player.direction.y > 0: 
					player.hit_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.hit_rect.top = sprite.rect.bottom
					player.direction.y = 0

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def check_bones(self):
		bones_hit = len(pg.sprite.spritecollide(self.player.sprite, self.bone_sprites, True))
		self.player.sprite.bones += bones_hit

	def reverse_enemies(self):
		for enemy in self.enemy_sprites.sprites():
			if pg.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def next_game_state(self):
		self.music[self.stage].stop()
		for sound in self.sfx:
			sound.stop()
		clicked_index = [i for i,button in enumerate(self.buttons) if button.clicked]
		return (self.states[clicked_index[0]],None)

	def check_enemy_death(self):
		for enemy in self.enemy_sprites.sprites():
			bark_range = abs(self.player.sprite.rect.centerx - enemy.rect.centerx)
			if self.player.sprite.barking and bark_range < 100:
				self.enemy_dust.add(ParticleEffect(enemy.rect.center, 'explosion'))
				enemy.kill()

	def bad_collision(self):
		damage = self.player.sprite.get_damage()
		if damage:
			self.current_health += damage

	def check_fail(self):
		if pg.sprite.spritecollide(self.player.sprite, self.danger_sprites, False):
			self.bad_collision()
		if pg.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False):
			self.bad_collision()

		if self.player.sprite.rect.top > HEIGHT or self.current_health <= 0:
			self.buttons[0].clicked = True
			self.completed = False
			self.is_over = True

	def check_win(self):
		if self.goal.sprite.is_open:
			if pg.sprite.spritecollide(self.player.sprite, self.goal, False):
				self.buttons[0].clicked = True
				self.completed = True
				self.is_over = True

	def update(self, event_info):
		super().update(event_info)
		self.scroll_x()

		# tile updates
		self.particle_sprite.update(self.world_shift)
		self.ground_sprites.update(self.world_shift)
		self.decoration_sprites.update(self.world_shift)
		self.gate_sprites.update(self.world_shift)
		self.bone_sprites.update(self.world_shift)
		self.danger_sprites.update(self.world_shift)
		self.check_enemy_death()
		self.enemy_dust.update(self.world_shift)
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.goal.update(self.world_shift)

		# check game over
		self.check_win()
		self.check_fail()

		# update ui
		self.health_bar.update(event_info,self.current_health)
		self.bone_bar.update(event_info,self.player.sprite.bones)

	def draw(self, display_screen):
		display_screen.blit(self.bg[self.stage], (0,0))
		display_screen.blit(self.bg[self.stage], (WIDTH/2,0))

		self.treasure_sprites.update(self.world_shift, display_screen)

		# draw tiles behind player
		self.decoration_sprites.draw(display_screen)
		self.gate_sprites.draw(display_screen)
		self.goal.draw(display_screen)
		self.treasure_sprites.draw(display_screen)
		self.bone_sprites.draw(display_screen)
		self.particle_sprite.draw(display_screen)
		self.ground_sprites.draw(display_screen)
		self.enemy_dust.draw(display_screen)

		self.player.update(display_screen)
		self.check_bones()
		
		# player
		self.horizontal_movement_collision()
		self.get_player_on_ground() # on ground before collision
		self.vertical_movement_collision()
		self.create_landing_dust()  # on ground after collision
		self.player.draw(display_screen)

		# draw tiles in front of player
		self.danger_sprites.draw(display_screen)
		self.reverse_enemies()
		self.enemy_sprites.draw(display_screen)

		# draw buttons
		for button in self.buttons:
			button.draw(display_screen)

		# draw UI
		self.health_bar.draw(display_screen)
		self.bone_bar.draw(display_screen)

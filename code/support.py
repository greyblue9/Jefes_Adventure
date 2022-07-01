from os import walk
import pygame as pg
from csv import reader
from settings import TILE_SIZE

def import_folder(path, type):
	file_list = []

	for _,__,files in walk(path):
		
		# remove mac's hidden file and sort in order
		if ".DS_Store" in files:
			files.remove(".DS_Store")
		files.sort()

		for item in files:
			full_path = path + '/' + item

			if type == "image":
				file = pg.image.load(full_path).convert_alpha()
			elif type == "sound":
				file = pg.mixer.Sound(full_path)

			file_list.append(file)
	return file_list

def import_csv(path):
	sprite_map = []
	with open(path) as map:
		level = reader(map,delimiter = ",")
		for row in level:
			sprite_map.append(list(row))
	return sprite_map

def import_cut_graphic(path):
	surface = pg.image.load(path).convert_alpha()
	tile_x = int(surface.get_size()[0] / TILE_SIZE)
	tile_y = int(surface.get_size()[1] / TILE_SIZE)

	cut_tiles = []
	for row in range(tile_y):
		for col in range(tile_x):
			x = col * TILE_SIZE
			y = row * TILE_SIZE
			new_surface = pg.Surface((TILE_SIZE,TILE_SIZE), flags = pg.SRCALPHA) 
			new_surface.blit(surface,(0,0),pg.Rect(x,y,TILE_SIZE,TILE_SIZE))
			cut_tiles.append(new_surface)
	return cut_tiles

def import_cursors(path):
	cursor_list = []

	for _,__,files in walk(path):
		
		# remove mac's hidden file and sort in order
		if ".DS_Store" in files:
			files.remove(".DS_Store")
		files.sort()

		for item in files:
			surface = pg.image.load(path + '/' + item).convert_alpha()
			cursor = pg.cursors.Cursor((20, 5), surface)
			cursor_list.append(cursor)
	return cursor_list
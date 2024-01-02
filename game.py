from grid import Grid
from blocks import *
from constants import *
import random
import pygame as pg
import sys


class Game:
	def __init__(self):
		pg.display.set_mode((500, 620))
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.score = 0
		self.rotate_sound = pg.mixer.Sound("Sounds/rotate.ogg")
		self.clear_sound = pg.mixer.Sound("Sounds/clear.ogg")

		pg.mixer.music.load("Sounds/main_theme.mp3")
		pg.mixer.music.play(-1)

	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		self.score += move_down_points

	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() is False or self.block_fits() is False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() is False or self.block_fits() is False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() is False or self.block_fits() is False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() is False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) is False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() is False or self.block_fits() is False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) is False:
				return False
		return True

	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)
		else:
			self.next_block.draw(screen, 270, 270)

	def play_game(self):
		GAME_UPDATE = pg.USEREVENT
		pg.time.set_timer(GAME_UPDATE, 450)

		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()
				if event.type == pg.KEYDOWN:
					if self.game_over is True:
						self.game_over = False
						self.reset()
					if event.key == pg.K_LEFT and self.game_over is False:
						self.move_left()
					if event.key == pg.K_RIGHT and self.game_over is False:
						self.move_right()
					if event.key == pg.K_DOWN and self.game_over is False:
						self.move_down()
						self.update_score(0, 1)
					if event.key == pg.K_UP and self.game_over is False:
						self.rotate()
				if event.type == GAME_UPDATE and self.game_over is False:
					self.move_down()

			score_value_surface = title_font.render(str(self.score), True, Colors.white)
			screen.fill(Colors.dark_blue)
			screen.blit(score_surface, (365, 20, 50, 50))
			screen.blit(next_surface, (375, 180, 50, 50))

			if self.game_over is True:
				screen.blit(game_over_surface, (320, 450, 50, 50))

			pg.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
			screen.blit(score_value_surface,
						score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
			pg.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
			self.draw(screen)

			pg.display.update()
			clock.tick(60)

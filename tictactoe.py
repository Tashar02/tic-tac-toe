# SPDX-FileCopyrightText: 2024-2025 Tashfin Shakeer Rhythm <tashfinshakeerrhythm@gmail.com>
# SPDX-License-Identifier: MIT

import pygame as pg, sys, time, os
from urllib import request
from collections import deque

# AssetManager - Manages game assets including downloading and loading
class AssetManager:
	ASSET_URLS = {
		"x.png": "https://raw.githubusercontent.com/Tashar02/tic-tac-toe/main/x.png",
		"o.png": "https://raw.githubusercontent.com/Tashar02/tic-tac-toe/main/o.png",
		"bg.png": "https://raw.githubusercontent.com/Tashar02/tic-tac-toe/main/bg.png",
	}

	def __init__(self, cell_size, screen_size):
		self.cell_size = cell_size
		self.screen_size = screen_size
		self.download_assets()
		self.load_assets()

	# download_assets() - Downloads missing assets from GitHub
	# Returns: None
	def download_assets(self):
		for filename, url in self.ASSET_URLS.items():
			if not os.path.exists(filename):
				try:
					print(f"\nDownloading {filename}...")
					request.urlretrieve(url, filename)
				except Exception as e:
					print(f"Error downloading {filename}: {e}")
					print("Exiting program!")
					pg.quit()
					sys.exit()

	# load_assets() - Load and scale game assets
	# Returns: None
	def load_assets(self):
		self.x_img = self.load_scaled_image("x.png")
		self.o_img = self.load_scaled_image("o.png")
		self.bg_img = pg.transform.scale(pg.image.load("bg.png"), 
						(self.screen_size, self.screen_size))

	# load_scaled_image() - Helper method to load and scale images
	# Returns: pygame.Surface
	def load_scaled_image(self, filename):
		return pg.transform.scale(
			pg.image.load(filename),
			(self.cell_size - self.cell_size // 4, self.cell_size - self.cell_size // 4)
		)

# GameBoard - Handles game board state and rendering
class GameBoard:
	def __init__(self, screen, assets, width, height, cell_size):
		self.screen = screen
		self.assets = assets
		self.width = width
		self.height = height
		self.cell_size = cell_size
		self.line_width = 15
		self.colors = {
			'bg': (63, 84, 72),
			'grid': (35, 48, 40),
			'win_line': (66, 66, 66),
			'text': (255, 255, 255)
		}
		self.game_initiating_window()

	# game_initiating_window() - Reset game state
	# Returns: None
	def game_initiating_window(self):
		self.board = [[None] * 3 for i in range(3)]
		self.game_over = False
		self.winning_line = None

	# draw_grid() - Draw tic-tac-toe grid lines
	# Returns: None
	def draw_grid(self):
		# Horizontal lines
		pg.draw.line(self.screen, self.colors['grid'], 
				(0, self.cell_size), (self.width, self.cell_size), self.line_width)
		pg.draw.line(self.screen, self.colors['grid'], 
				(0, 2 * self.cell_size), (self.width, 2 * self.cell_size), self.line_width)
		# Vertical lines
		pg.draw.line(self.screen, self.colors['grid'], 
				(self.cell_size, 0), (self.cell_size, self.height), self.line_width)
		pg.draw.line(self.screen, self.colors['grid'], 
				(2 * self.cell_size, 0), (2 * self.cell_size, self.height), self.line_width)

	# drawXO() - Draw all X/O symbols on the board
	# Returns: None
	def drawXO(self):
		for row in range(3):
			for col in range(3):
				if self.board[row][col] == "X":
					x_pos = col * self.cell_size + self.cell_size // 8
					y_pos = row * self.cell_size + self.cell_size // 8
					self.screen.blit(self.assets.x_img, (x_pos, y_pos))
				elif self.board[row][col] == "O":
					x_pos = col * self.cell_size + self.cell_size // 8
					y_pos = row * self.cell_size + self.cell_size // 8
					self.screen.blit(self.assets.o_img, (x_pos, y_pos))

	# draw_winning_line() - Draw winning line if present
	# Returns: None
	def draw_winning_line(self):
		if self.winning_line:
			line_type, pos = self.winning_line
			if line_type == "vertical":
				pg.draw.line(self.screen, self.colors['win_line'],
						(pos * self.cell_size + self.cell_size // 2, 15),
						(pos * self.cell_size + self.cell_size // 2, self.height - 15),
						self.line_width)
			elif line_type == "horizontal":
				pg.draw.line(self.screen, self.colors['win_line'],
						(15, pos * self.cell_size + self.cell_size // 2),
						(self.width - 15, pos * self.cell_size + self.cell_size // 2),
						self.line_width)
			elif line_type == "asc_diagonal":
				pg.draw.line(self.screen, self.colors['win_line'],
						(15, self.height - 15), (self.width - 15, 15), self.line_width)
			elif line_type == "desc_diagonal":
				pg.draw.line(self.screen, self.colors['win_line'],
						(15, 15), (self.width - 15, self.height - 15), self.line_width)

# TicTacToeGame - Main game controller
class TicTacToeGame:
	def __init__(self):
		# Game constants
		self.SCREEN_SIZE = 600
		self.CELL_SIZE = self.SCREEN_SIZE // 3
		self.STATUS_HEIGHT = 100

		# Initialize pygame
		pg.init()
		self.screen = pg.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE + self.STATUS_HEIGHT))
		pg.display.set_caption("Tic Tac Toe")

		# Initialize components
		self.assets = AssetManager(self.CELL_SIZE, self.SCREEN_SIZE)
		self.board = GameBoard(self.screen, self.assets, 
				      self.SCREEN_SIZE, self.SCREEN_SIZE, self.CELL_SIZE)
		self.players = deque(['X', 'O'])
		self.current_player = self.players[0]
		self.font = pg.font.Font(None, 40)
		self.starting_player = 'X'

	# game_status() - Update game status text
	# Returns: None
	def game_status(self):
		if self.board.game_over:
			winner = self.check_winner()
			status = (f"Player {winner} Wins! Press R to Restart" if winner 
				 else "It's a Draw! Press R to Restart")
		else:
			status = f"Player {self.current_player}'s Turn"

		text = self.font.render(status, True, self.board.colors['text'], self.board.colors['bg'])
		self.screen.fill(self.board.colors['bg'], (0, self.SCREEN_SIZE, self.SCREEN_SIZE, self.STATUS_HEIGHT))
		self.screen.blit(text, (20, self.SCREEN_SIZE + 30))

	# check_winner() - Check for winning conditions
	# Returns: str (winner) or None
	def check_winner(self):
		# Check rows and columns
		for i in range(3):
			if self.board.board[i][0] == self.board.board[i][1] == self.board.board[i][2] and self.board.board[i][0]:
				self.board.winning_line = ("horizontal", i)
				return self.board.board[i][0]
			if self.board.board[0][i] == self.board.board[1][i] == self.board.board[2][i] and self.board.board[0][i]:
				self.board.winning_line = ("vertical", i)
				return self.board.board[0][i]

		# Check diagonals
		if self.board.board[0][0] == self.board.board[1][1] == self.board.board[2][2] and self.board.board[0][0]:
			self.board.winning_line = ("desc_diagonal", None)
			return self.board.board[0][0]
		if self.board.board[0][2] == self.board.board[1][1] == self.board.board[2][0] and self.board.board[0][2]:
			self.board.winning_line = ("asc_diagonal", None)
			return self.board.board[0][2]
		return None

	# check_draw() - Check if game is a draw
	# Returns: bool
	def check_draw(self):
		return all(all(cell for cell in row) for row in self.board.board)

	# user_click() - Process mouse click event
	# Returns: None
	def user_click(self, pos):
		if self.board.game_over:
			return

		x, y = pos
		if y < self.SCREEN_SIZE:
			row = y // self.CELL_SIZE
			col = x // self.CELL_SIZE

			if not self.board.board[row][col]:
				self.board.board[row][col] = self.current_player

				if self.check_winner() or self.check_draw():
					self.board.game_over = True
				else:
					self.players.rotate(-1)
					self.current_player = self.players[0]

	# reset_game() - Reset game state with alternating starting player
	# Returns: None
	def reset_game(self):
		self.board.game_initiating_window()
		self.starting_player = 'O' if self.starting_player == 'X' else 'X'
		self.players = deque([self.starting_player, 'O' if self.starting_player == 'X' else 'X'])
		self.current_player = self.players[0]
		self.screen.blit(self.assets.bg_img, (0, 0))
		self.board.draw_grid()
		pg.display.update()

	# event_handler() - Handle input events
	# Returns: None
	def event_handler(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				self.user_click(pg.mouse.get_pos())
			if event.type == pg.KEYDOWN and event.key == pg.K_r:
				self.reset_game()

	# update_display() - Update game display
	# Returns: None
	def update_display(self):
		self.board.drawXO()
		self.board.draw_winning_line()
		self.game_status()
		pg.display.update()

	# run() - Main game loop
	# Returns: None
	def run(self):
		# Initial draw
		self.screen.blit(self.assets.bg_img, (0, 0))
		self.board.draw_grid()
		pg.display.update()

		while True:
			self.event_handler()
			self.update_display()
			time.sleep(0.1)

if __name__ == "__main__":
	print("\nStarting the program...")
	game = TicTacToeGame()
	game.run()

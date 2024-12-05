import pygame as pg, sys, time

# Initialize pygame
pg.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)

# Initialize screen
screen = pg.display.set_mode((WIDTH, HEIGHT + 100))
pg.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Load assets for X and O
x_img = pg.transform.scale(pg.image.load('x.png'), (CELL_SIZE - SPACE, CELL_SIZE - SPACE))
y_img = pg.transform.scale(pg.image.load('o.png'), (CELL_SIZE - SPACE, CELL_SIZE - SPACE))

# Load font for displaying text
font = pg.font.Font(None, 40)

# Store all game data in a dictionary
game_data = {
	'board': [[None] * BOARD_COLS for i in range(BOARD_ROWS)],
	'updated_cells': [],
	'player': 'X',
	'game_over': False
}

# draw_lines() - Draws the grid lines for the tic-tac-toe board.
# Returns: None
def draw_lines():
	for row in range(1, BOARD_ROWS):
		# Horizontal lines
		pg.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), LINE_WIDTH)
		# Vertical lines
		pg.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), LINE_WIDTH)

# drawXO() - Renders X and O symbols for updated cells.
# Returns: None
def drawXO():
	for row, col in game_data['updated_cells']:
		img = y_img if game_data['board'][row][col] == 'O' else x_img
		screen.blit(img, (col * CELL_SIZE + SPACE // 2, row * CELL_SIZE + SPACE // 2))
	game_data['updated_cells'].clear()

# draw_vertical_winning_line() - Draws a vertical line for the winner.
# Returns: None
def draw_vertical_winning_line(col, player):
	posX = col * CELL_SIZE + CELL_SIZE // 2
	color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
	pg.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

# draw_horizontal_winning_line() - Draws a horizontal line for the winner.
# Returns: None
def draw_horizontal_winning_line(row, player):
	posY = row * CELL_SIZE + CELL_SIZE // 2
	color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
	pg.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

# draw_asc_diagonal() - Draws a diagonal line from bottom-left to top-right for the winner.
# Returns: None
def draw_asc_diagonal(player):
	color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
	pg.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

# draw_desc_diagonal() - Draws a diagonal line from top-left to bottom-right for the winner.
# Returns: None
def draw_desc_diagonal(player):
	color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
	pg.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

# check_winner() - Checks if there's a winner and draws the winning line.
# Returns: 'X' or 'O' if there's a winner, None otherwise.
def check_winner():
	# Check for a winner in rows and columns
	for i in range(BOARD_ROWS):
		if game_data['board'][i][0] == game_data['board'][i][1] == game_data['board'][i][2] and game_data['board'][i][0]:
			draw_horizontal_winning_line(i, game_data['board'][i][0])
			return game_data['board'][i][0]
		if game_data['board'][0][i] == game_data['board'][1][i] == game_data['board'][2][i] and game_data['board'][0][i]:
			draw_vertical_winning_line(i, game_data['board'][0][i])
			return game_data['board'][0][i]

	# Check for a winner in diagonals
	if game_data['board'][0][0] == game_data['board'][1][1] == game_data['board'][2][2] and game_data['board'][0][0]:
		draw_desc_diagonal(game_data['board'][0][0])
		return game_data['board'][0][0]
	if game_data['board'][0][2] == game_data['board'][1][1] == game_data['board'][2][0] and game_data['board'][0][2]:
		draw_asc_diagonal(game_data['board'][0][2])
		return game_data['board'][0][2]

	return None

# check_draw() - Checks if the game is a draw (board is full but no winner).
# Returns: True if draw, False otherwise.
def check_draw():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if game_data['board'][row][col] is None:
				return False
	return True

# game_status() - Displays the current game status (whose turn or the winner).
# Returns: None
def game_status():
	status = "Player X's Turn" if game_data['player'] == 'X' else "Player O's Turn"
	if game_data['game_over']:
		winner = check_winner()
		if winner:
			status = f"Player {winner} Wins! Press R to Restart"
		elif check_draw():
			status = "It's a Draw! Press R to Restart"
	text = font.render(status, True, TEXT_COLOR, BG_COLOR)
	screen.fill(BG_COLOR, (0, HEIGHT, WIDTH, 100))
	screen.blit(text, (20, HEIGHT + 20))

# user_click() - Handles mouse clicks and updates the game state.
# Returns: None
def user_click():
	mouseX, mouseY = pg.mouse.get_pos()
	if mouseY < HEIGHT:
		clicked_row = mouseY // CELL_SIZE
		clicked_col = mouseX // CELL_SIZE

		if not game_data['board'][clicked_row][clicked_col]:
			game_data['board'][clicked_row][clicked_col] = game_data['player']
			game_data['updated_cells'].append((clicked_row, clicked_col))
			if check_winner() or check_draw():
				game_data['game_over'] = True
			game_data['player'] = 'O' if game_data['player'] == 'X' else 'X'
			game_status()

# game_initiating_window() - Initializes a new match for the game.
# Returns: None
def game_initiating_window():
	screen.fill(BG_COLOR)
	draw_lines()
	game_data['updated_cells'].clear()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			game_data['board'][row][col] = None

# reset_game() - Resets the game.
# Returns: None
def reset_game():
	game_initiating_window()
	game_data['game_over'] = False
	game_data['player'] = 'X'
	game_status()

# event_handler - Handles input events and modifies the game state.
# Returns: None
def event_handler():
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()

		if event.type == pg.MOUSEBUTTONDOWN and not game_data['game_over']:
			user_click()

		if event.type == pg.KEYDOWN and event.key == pg.K_r:
			reset_game()

# update_display - Updates the game display in response to inputs.
# Returns: None
def update_display():
	drawXO()
	game_status()
	pg.display.update()

## Begin Tic Tac Toe
# Initial game board setup
game_initiating_window()

# Start the match
while True:
	# Handle user input events
	event_handler()

	# Draw and update the game display
	update_display()

	# Time interval for a player to provide input after another
	time.sleep(0.1)

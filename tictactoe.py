import pygame as pg, sys, time

# Initialize pygame
pg.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

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

# Board state
board = [[None] * BOARD_COLS for i in range(BOARD_ROWS)]

# Load assets for X and O
x_img = pg.transform.scale(pg.image.load('x.png'), (150, 150))
y_img = pg.transform.scale(pg.image.load('o.png'), (150, 150))

# Load font for displaying text
font = pg.font.Font(None, 40)

# draw_lines() - Draws the grid lines for the tic-tac-toe board.
# Returns: None
def draw_lines():
	for row_num in range(1, BOARD_ROWS):
		# Horizontal lines
		pg.draw.line(screen, LINE_COLOR, (0, row_num * 200), (WIDTH, row_num * 200), LINE_WIDTH)
		# Vertical lines
		pg.draw.line(screen, LINE_COLOR, (row_num * 200, 0), (row_num * 200, HEIGHT), LINE_WIDTH)

# drawXO() - Renders X and O symbols.
# Returns: None
def drawXO(row, col):
	if board[row][col] == 'O':
		screen.blit(y_img, (col * 200 + 25, row * 200 + 25))
	elif board[row][col] == 'X':
		screen.blit(x_img, (col * 200 + 25, row * 200 + 25))

# check_winner() - Draws the winning line if a winner exists.
# Returns: 'X' or 'O' if there's a winner, None otherwise.
def check_winner():
	# Check for a winner in rows and columns
	for i in range(BOARD_ROWS):
		if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
			draw_horizontal_winning_line(i, board[i][0])
			return board[i][0]
		if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
			draw_vertical_winning_line(i, board[0][i])
			return board[0][i]

	# Check for a winner in diagonals
	if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
		draw_desc_diagonal(board[0][0])
		return board[0][0]
	if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
		draw_asc_diagonal(board[0][2])
		return board[0][2]

	return None

# check_draw() - Checks if the game is a draw (board is full but no winner).
# Returns: True if draw, False otherwise.
def check_draw():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] is None:
				return False
	return True

# draw_status() - Displays the current game status (whose turn or the winner).
# Returns: None
def draw_status():
	status = "Player X's Turn" if player == 'X' else "Player O's Turn"
	if game_over:
		winner = check_winner()
		if winner:
			status = f"Player {winner} Wins! Press R to Restart"
		elif check_draw():
			status = "It's a Draw! Press R to Restart"
	text = font.render(status, True, TEXT_COLOR, BG_COLOR)
	screen.fill(BG_COLOR, (0, HEIGHT, WIDTH, 100))
	screen.blit(text, (20, HEIGHT + 20))

# draw_vertical_winning_line() - Draws a vertical line for the winner.
# Returns: None
def draw_vertical_winning_line(col, player):
	posX = col * 200 + 100
	color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
	pg.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

# draw_horizontal_winning_line() - Draws a horizontal line for the winner.
# Returns: None
def draw_horizontal_winning_line(row, player):
	posY = row * 200 + 100
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

# user_click() - Handles mouse clicks and updates the game state.
# Returns: None
def user_click():
	mouseX, mouseY = pg.mouse.get_pos()
	if mouseY < HEIGHT:
		clicked_row = mouseY // 200
		clicked_col = mouseX // 200

		if not board[clicked_row][clicked_col]:
			global player
			board[clicked_row][clicked_col] = player
			if check_winner() or check_draw():
				global game_over
				game_over = True
			player = 'O' if player == 'X' else 'X'
			draw_status()

# game_initiating_window() - Resets the game state to start a new match.
# Returns: None
def game_initiating_window():
	screen.fill(BG_COLOR)
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = None

# Main loop variables
player = 'X'
game_over = False

# Initial setup
game_initiating_window()
draw_status()

# Main loop
while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()

		if event.type == pg.MOUSEBUTTONDOWN and not game_over:
			user_click()

		if event.type == pg.KEYDOWN and event.key == pg.K_r:
			game_initiating_window()
			game_over = False
			player = 'X'
			draw_status()

	# Draw X and O symbols at the right positions
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col]:
				drawXO(row, col)

	pg.display.update()
	time.sleep(0.1)

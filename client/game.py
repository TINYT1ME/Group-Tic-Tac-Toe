import pygame

# Initialize pygame
pygame.init()

# Define the screen size
screen_size = (300, 300)

# Create the screen
screen = pygame.display.set_mode(screen_size)

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Define the game board
board = [[" " for i in range(3)] for j in range(3)]

# Define the font
font = pygame.font.Font(None, 72)

# Initialize the turn
turn = "X"

# Initialize the game over flag
game_over = False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            row = y // 100
            col = x // 100
            if board[row][col] == " ":
                board[row][col] = turn
                if turn == "X":
                    turn = "O"
                else:
                    turn = "X"

    screen.fill(white)

    for i in range(3):
        for j in range(3):
            text = font.render(board[i][j], True, black)
            screen.blit(text, (j * 100 + 25, i * 100 + 25))

    pygame.draw.line(screen, black, (100, 0), (100, 300), 5)
    pygame.draw.line(screen, black, (200, 0), (200, 300), 5)
    pygame.draw.line(screen, black, (0, 100), (300, 100), 5)
    pygame.draw.line(screen, black, (0, 200), (300, 200), 5)

    pygame.display.update()

# Quit pygame
pygame.quit()


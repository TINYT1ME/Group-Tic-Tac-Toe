import pygame


# Initialize the game over flag
game_over = False


def get_click():
    pygame.init()

    # Define the WIN size
    WIN_size = (300, 300)

    # Create the WIN
    WIN = pygame.display.set_mode(WIN_size)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                row = y // 100
                col = x // 100
                return row, col

def draw_window(board, font, small_font, WIN, black, white, team):
    WIN.fill(white)

    # draw board
    for i in range(3):
        for j in range(3):
            text = font.render(board[i][j], True, black)
            WIN.blit(text, (j * 100 + 25, i * 100 + 25))

    # Show which team you are on top left corner
    if team == 0:
        text = small_font.render("Team: X", True, black)
    else:
        text = small_font.render("Team: O", True, black)
    WIN.blit(text, (0, 0))
    

    # Draw board lines
    pygame.draw.line(WIN, black, (100, 0), (100, 300), 5)
    pygame.draw.line(WIN, black, (200, 0), (200, 300), 5)
    pygame.draw.line(WIN, black, (0, 100), (300, 100), 5)
    pygame.draw.line(WIN, black, (0, 200), (300, 200), 5)

    # update screen
    pygame.display.update()


def main(board, team):
    global x_value
    global y_value
    # Initialize pygame
    pygame.init()

    # Define the WIN size
    WIN_size = (300, 300)

    # Create the WIN
    WIN = pygame.display.set_mode(WIN_size)

    # Define colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Define the game board
    #board = [[" " for i in range(3)] for j in range(3)]

    # Define the font
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 24)

    # Main game loop
    while not game_over:
 #       for event in pygame.event.get():
 #           if event.type == pygame.MOUSEBUTTONUP:
 #               x, y = pygame.mouse.get_pos()
 #               row = y // 100
 #               col = x // 100
 #               x_value = col
 #               y_value = row
 #
        draw_window(board, font, small_font, WIN, black, white, team)

# Quit pygame
pygame.quit()


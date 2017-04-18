"""
Simulation of Game of Life with pygame
"""
import pygame
from pygame.locals import *
import numpy as np

__author__ = "Davide Tonin"

game_ended = False; game_stop = False; FPS = 60; CELL_SIZE = 20
total_cells, alive_cells = 0, 0
game_board = None
board_changed = False; stop_transition = False
color = "red"


def init_board():
    """Initialize the game board with random alive and dead cells"""
    global game_board
    game_board = np.random.randint(2, size=(HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE))


def game_board_transition():
    """Parse the game board, count neighbours and do the transition to the next step"""
    global game_board, game_ended, alive_cells
    previous_game_board = np.copy(game_board)
    alive_cells = 0
    for row in range(game_board.shape[0]):
        for column in range(game_board[row].shape[0]):
            alive_neighbours = 0
            # control of  the above row
            if row > 0:
                if column > 0 and previous_game_board[row-1][column-1] > 0: alive_neighbours += 1
                if previous_game_board[row-1][column] > 0: alive_neighbours += 1

                try:
                    if previous_game_board[row-1][column+1] > 0: alive_neighbours += 1
                except IndexError: pass

            # control of the right neighbours
            try:
                if previous_game_board[row][column+1] > 0: alive_neighbours += 1
            except IndexError: pass

            # control of the below row
            try:
                if previous_game_board[row+1][column+1] > 0: alive_neighbours += 1
            except IndexError: pass

            try:
                if previous_game_board[row+1][column] > 0: alive_neighbours += 1
            except IndexError: pass

            if column > 0:
                try:
                    if previous_game_board[row+1][column-1] > 0: alive_neighbours += 1
                except IndexError: pass

                # control of the left neighbours
                try:
                    if previous_game_board[row][column-1] > 0: alive_neighbours += 1
                except IndexError: pass
            
            if game_board[row][column] > 0:
                if alive_neighbours == 2 or alive_neighbours == 3:
                    if game_board[row][column] < 6: game_board[row][column] += 1
                else: game_board[row][column] = 0
            else:
                if alive_neighbours == 3: game_board[row][column] = 1

            if game_board[row][column] > 0: alive_cells += 1


def resize_board(action):
    """ Resize the game board """
    global game_board, CELL_SIZE
    if action == "+": CELL_SIZE += 1
    else: CELL_SIZE -= 1

    new_game_board = np.zeros((HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE), dtype=int)

    for row in range(game_board.shape[0]):
        for column in range(game_board[row].shape[0]):
            try: new_game_board[row][column] = game_board[row][column]
            except: pass

    game_board = np.copy(new_game_board)



def draw_game_board():
    """Draw the game board"""
    global game_window, game_board, color

    for row in range(game_board.shape[0]):
        for column in range(game_board[row].shape[0]):
            if game_board[row][column] > 0:
                if color == "red": alive_color = (game_board[row][column]*40, 0, 0)
                elif color == "green": alive_color = (0, game_board[row][column]*40, 0)
                elif color == "blue": alive_color = (0, 0, game_board[row][column]*40)
                elif color == "cyan": alive_color = (0, game_board[row][column]*40, game_board[row][column]*40)
                elif color == "white":alive_color = (game_board[row][column] * 40, game_board[row][column] * 40, game_board[row][column] * 40)
                pygame.draw.rect(game_window, alive_color, [column*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE])


if __name__ == '__main__':
    pygame.init()

    GAME_RESOLUTION = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    game_window = pygame.display.set_mode(GAME_RESOLUTION, FULLSCREEN|HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption("PyGameOfLife, "+__author__)
    clock = pygame.time.Clock()

    pygame.font.init()
    text_settings = pygame.font.SysFont("Open Sans", 25)

    init_board(); stop_transition = True

    while not game_ended:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_ended = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_F4: game_ended = True
                if event.key == K_RETURN:                      init_board(); board_changed = True; stop_transition = True
                if event.key == K_SPACE:                       game_stop = not game_stop
                if event.key == K_r:                           color = "red"; board_changed = True; stop_transition = True
                if event.key == K_g:                           color = "green"; board_changed = True; stop_transition = True
                if event.key == K_b:                           color = "blue"; board_changed = True; stop_transition = True
                if event.key == K_c:                           color = "cyan"; board_changed = True; stop_transition = True
                if event.key == K_w:                           color = "white"; board_changed = True; stop_transition = True
                if event.key == K_p or event.key == K_PLUS:    resize_board("+"); board_changed = True
                if event.key == K_m or event.key == K_MINUS:   resize_board("-"); board_changed = True

        if not game_stop or board_changed == True:
            pygame.Surface.fill(game_window, (0, 0, 0))


            if not stop_transition: game_board_transition()
            else: stop_transition = not stop_transition
            draw_game_board()

            total_cells = (WIDTH // CELL_SIZE) * (HEIGHT // CELL_SIZE)

            game_window.blit(text_settings.render("FPS: "+str(round(clock.get_fps(), 2)), True, (255, 255, 255)), (20, 20))
            game_window.blit(text_settings.render("Total cells: "+str(total_cells), True, (255, 255, 255)), (20, 50))
            game_window.blit(text_settings.render("Alive cells: " + str(alive_cells)+", "+str(round(alive_cells*100/total_cells, 2))+"%", True,(255, 255, 255)), (20, 80))

            if board_changed: board_changed = not board_changed
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    exit()
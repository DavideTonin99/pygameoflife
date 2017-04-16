"""
Simulation of Game of Life with pygame
"""
import pygame
from pygame.locals import *
import numpy as np

__author__ = "Davide Tonin"
__version__ = "1.0"

game_ended = False; FPS = 60; CELL_SIZE = 20
game_board = None
color = "red"


def init_board():
    """Initialize the game board with random alive and dead cells"""
    global game_board
    game_board = np.random.randint(2, size=(HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE))


def game_board_transition():
    """Parse the game board, count neighbours and do the transition to the next step"""
    global game_board, game_ended
    previous_game_board = np.copy(game_board)

    for row in np.arange(0, game_board.shape[0]):
        for column in np.arange(0, game_board[row].shape[0]):
            alive_neighbours = 0
            if row > 0:
                if column > 0 and previous_game_board[row-1][column-1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
                if previous_game_board[row-1][column] > 0: alive_neighbours = np.sum([alive_neighbours, 1])

                try:
                    if previous_game_board[row-1][column+1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
                except IndexError: pass

            try:
                if previous_game_board[row][column+1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
            except IndexError: pass

            try:
                if previous_game_board[row+1][column+1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
            except IndexError: pass

            try:
                if previous_game_board[row+1][column] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
            except IndexError: pass

            if column > 0:
                try:
                    if previous_game_board[row+1][column-1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
                except IndexError: pass

                try:
                    if previous_game_board[row][column-1] > 0: alive_neighbours = np.sum([alive_neighbours, 1])
                except IndexError: pass

            if game_board[row][column] > 0:
                if alive_neighbours == 2 or alive_neighbours == 3:
                    if game_board[row][column] < 6:
                        game_board[row][column] = np.sum([game_board[row][column], 1])
                else:
                    game_board[row][column] = 0
            else:
                if alive_neighbours == 3: game_board[row][column] = 1


def draw_game_board(game_window):
    """Draw the game board"""
    global game_board, color
    for row in np.arange(0, game_board.shape[0]):
        for column in np.arange(0, game_board[row].shape[0]):
            if game_board[row][column] > 0:
                if color == "red": alive_color = (game_board[row][column]*40, 0, 0)
                elif color == "green": alive_color = (0, game_board[row][column]*40, 0)
                else: alive_color = (0, 0, game_board[row][column]*40)
                pygame.draw.rect(game_window, alive_color, [column*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE])


if __name__ == '__main__':
    pygame.init()

    GAME_RESOLUTION = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    game_window = pygame.display.set_mode(GAME_RESOLUTION, FULLSCREEN|HWACCEL|HWSURFACE)
    clock = pygame.time.Clock()

    pygame.font.init()

    init_board()

    while not game_ended:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_F4:
                    game_ended = True
                if event.key == K_RETURN or event.key == K_SPACE:
                    init_board()
                if event.key == K_r:
                    color = "red"
                if event.key == K_g:
                    color = "green"
                if event.key == K_b:
                    color = "blue"
        pygame.Surface.fill(game_window, (0, 0, 0))

        game_board_transition()
        draw_game_board(game_window)

        game_window.blit(
            pygame.font.SysFont("Open Sans", 30).render("FPS: "+str(round(clock.get_fps(), 2)), 1, (255, 255, 255)), (20, 20))
        game_window.blit(
            pygame.font.SysFont("Open Sans", 30).render("Press SPACE or RETURN to restart the game", 1, (255, 255, 255)), (20, 50))
        game_window.blit(
            pygame.font.SysFont("Open Sans", 30).render(
                "Press r (red), g (green), b (blue)", 1, (255, 255, 255)), (20, HEIGHT-40))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    exit()
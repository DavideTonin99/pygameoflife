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


def init_board():
    """Initialize the game board with random alive and dead cells"""
    global game_board
    game_board = np.random.randint(2, size=(HEIGHT//CELL_SIZE, WIDTH//CELL_SIZE))


def parse_game_board():
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

            if previous_game_board[row][column] > 0:
                if alive_neighbours == 2 or alive_neighbours == 3:
                    if game_board[row][column] < 12:
                        game_board[row][column] = np.sum([game_board[row][column], 1])
                else:
                    game_board[row][column] = 0
            else:
                if alive_neighbours == 3: game_board[row][column] = 1


def draw_game_board(game_window):
    """Draw the game board"""
    global game_board
    for row in np.arange(0, game_board.shape[0]):
        for column in np.arange(0, game_board[row].shape[0]):
            # green = 0 if game_board[row][column] > 0 else 0
            # blue = 0 if game_board[row][column] > 0 else 0
            green = 0
            blue = 0
            red = game_board[row][column]*20
            pygame.draw.rect(game_window, (red, green, blue), [column*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE])


if __name__ == '__main__':
    pygame.init()
    GAME_RESOLUTION = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    game_window = pygame.display.set_mode(GAME_RESOLUTION, FULLSCREEN|HWACCEL|HWSURFACE)
    clock = pygame.time.Clock()

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

        pygame.Surface.fill(game_window, (0, 0, 0))

        parse_game_board()
        draw_game_board(game_window)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    exit()
import pygame
from Timer import Timer
from os.path import join
from pygame.image import load
from random import choice

# game sizes
ROWS = 20
COLUMNS = 10
SIZE = 35
GAME_WIDTH, GAME_HEIGHT = COLUMNS * SIZE, ROWS * SIZE

# preview and score part
OTHER_BAR = 350
SCORE_HEIGHT_FRACTION = 0.7
PREVIEW_HEIGHT_FRACTION = 1 - SCORE_HEIGHT_FRACTION

# window size
WIDTH_PADDING = 25
HEIGHT_PADDING = 50
WINDOW_WIDTH = GAME_WIDTH + OTHER_BAR + 25 * 3
WINDOW_HEIGHT = GAME_HEIGHT + HEIGHT_PADDING * 2


# Game constants
UPDATE_TIMER_SPEED = 300
UPDATE_TIMER_MOVE = UPDATE_TOMER_ROTATE = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
VIOLET = (128, 0, 128)
BABY_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
BROWN = (255, 130, 0)
GRAY = (50, 50, 50)

COLORS_NUM = {
    VIOLET: 1,
    BABY_BLUE: 2,
    YELLOW: 3,
    GREEN: 4,
    RED: 5,
    BROWN: 6,
    BLUE: 7
}

NUMS_COLORS = {
    1: VIOLET,
    2: BABY_BLUE,
    3: YELLOW,
    4: GREEN,
    5: RED,
    6: BROWN,
    7: BLUE
}

# shapes
TETROMINOES = {
    'T': {'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': VIOLET},
    'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': BABY_BLUE},
    'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': YELLOW},
    'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': GREEN},
    'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': RED},
    'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': BROWN},
    'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': BLUE}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}

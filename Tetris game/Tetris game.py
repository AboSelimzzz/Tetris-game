import pygame as py
import numpy as np


BOARD = np.zeros((20, 10), dtype=int)
COLOR = np.empty((20, 10), dtype=tuple)
SHAPES = [
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
]
COLORS = [(128, 0, 128), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 130, 0), (0, 0, 255)]
SCORES = 0
LEVELS = 0

py.init()
window = py.display.set_mode((720, 720))
py.display.set_caption("Tetris Game")
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    window.fill((0, 0, 0))
    py.display.update()
py.quit()

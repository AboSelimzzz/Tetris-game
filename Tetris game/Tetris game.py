import pygame
import random
import numpy as np


def down_pressed(x_pos, y_pos):
    while True:
        new_x = (x_pos - start_x) % width
        new_y = (y_pos + height - start_y) % height
        if y_pos + height > last_y or board[new_x, new_y + 1] == 1:
            board[new_x, new_y] = 1
            y_pos += height
            break
        y_pos += height
    return y_pos


def check_done_rows(matrix):
    trans_board = np.transpose(matrix)
    index = [i for i in range(matrix.shape[0]) if np.all(trans_board[i] == 1)]
    for i in reversed(index):
        trans_board = np.delete(trans_board, i, axis=0)
        trans_board = np.vstack((np.zeros(matrix.shape[1]), trans_board))
    return np.transpose(trans_board)


def draw_tetris_board():
    for i in range(10):
        for j in range(10):
            if board[i][j] == 1:
                pygame.draw.rect(window, color_board[i][j], (start_x + (i * width), start_y + (j * height), width, height))


SHAPES = [
    np.array([[1, 1, 1], [0, 1, 0]]),   # T
    np.array([[1, 1, 1, 1]]),   # I
    np.array([[1, 1], [1, 1]]),   # o
    np.array([[0, 1, 1], [1, 1, 0]]),   # S
    np.array([[1, 1, 0], [0, 1, 1]])   # z
]
COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0)]
scores = 0
levels = 1
board = np.zeros((10, 10), dtype=int)
color_board = np.empty((10, 10), dtype=tuple)
pygame.init()
window = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Tetris Game")
running = True
start_x = 120
last_x = 534
start_y = 140
last_y = 554
width = height = 46
y = 100.0
x = start_x + width * 4
current_one = (random.choice(SHAPES), random.choice(COLORS))
while running:
    xx = int((x - start_x) / width)
    yy = round((int(y) - start_y) / height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if y < last_y:
                    y += 10  # down_pressed(x, y)
                    scores += 10
            if event.key == pygame.K_LEFT:
                if x > start_x:
                    if board[xx - 1, yy] == 0:
                        x -= width
            if event.key == pygame.K_RIGHT:
                if x < last_x:
                    if board[xx + 1, yy] == 0:
                        x += width
    y += 0.1
    if y >= last_y or (0 <= yy < 9 and board[xx][yy + 1] == 1):
        board[xx][yy] = 1
        color_board[xx][yy] = current_one[1]
        y = 100
        x = start_x + width * 4
        current_one = (random.choice(SHAPES), random.choice(COLORS))

    board = check_done_rows(board)
    window.fill((0, 0, 0))
    draw_tetris_board()
    pygame.draw.rect(window, current_one[1], (x, y, width, height))
    pygame.draw.lines(window, (255, 0, 0), False,
                      [(start_x - 5, start_y), (start_x - 5, last_y + width + 5),
                       (585, last_y + width + 5), (585, start_y)], 5)
    pygame.display.update()
pygame.quit()

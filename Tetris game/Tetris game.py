import pathlib
import pygame
import random
import numpy as np


def check_left_collision(x_ind, y_ind, piece):
    coll = False
    shape, _ = piece
    max_xs = []
    x_temp = x_ind
    for i in shape:
        done = False
        x_ind = x_temp
        for j in i:
            if not done or (j and done):
                x_ind += 1
                if j:
                    done = True
            if not j and done:
                break
        max_xs.append(x_ind)
    for max_x in max_xs:
        if board[max_x, y_ind]:
            coll = True
            break
    return coll


def check_collision(x_ind, y_ind, piece):
    coll = False
    shape, _ = piece
    x_temp = x_ind
    for i in shape:
        x_ind = x_temp
        for j in i:
            if j:
                if 0 < y_ind < 9 and board[x_ind][y_ind + 1] == 1:
                    coll = True
                    break
            x_ind += 1
        if coll:
            break
        y_ind += 1
    return coll


def check_events(x_pos, y_pos, sc, piece):
    r = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            r = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if y_pos + (len(piece[0]) - 1) * height < last_y:
                    y_pos += 20
                    sc += 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if x_pos > start_x:
                    if board[xx - 1, yy] == 0:
                        x_pos -= width
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if calc_max_x(piece, x_pos) <= last_x:
                    x_ind, y_ind = calc_xx_yy(x_pos, y_pos)
                    if not check_left_collision(x_ind, y_ind, piece):
                        x_pos += width
            if event.key == pygame.K_SPACE and rand != 2:
                piece = np.rot90(piece[0], 1, (1, 0)), piece[1]
    return r, x_pos, y_pos, sc, piece


def check_done_rows(matrix, sc, lev):
    trans_board = np.transpose(matrix)
    index = [ii for ii in range(matrix.shape[0]) if np.all(trans_board[ii] == 1)]
    for ii in reversed(index):
        trans_board = np.delete(trans_board, ii, axis=0)
        trans_board = np.vstack((np.zeros(matrix.shape[1]), trans_board))
    if index:
        sc += 100
        lev += len(index)
    if len(index) > 1:
        sc += 100
        if len(index) == 2:
            sc += 100
        if len(index) == 3:
            sc += 200
        if len(index) == 4:
            sc += 300
    return np.transpose(trans_board), sc, lev


def draw_tetris_board():
    for ii in range(10):
        for jj in range(10):
            if board[ii][jj] == 1:
                pygame.draw.rect(window, color_board[ii][jj],
                                 (start_x + (ii * width), start_y + (jj * height), width, height))


def draw_piece(piece, x_pos, y_pos):
    shape, color = piece
    x_temp = x_pos
    for ii in shape:
        for jj in ii:
            if jj:
                pygame.draw.rect(window, color, (x_pos, y_pos, width, height))
            x_pos += width
        y_pos += height
        x_pos = x_temp


def drawing_stuff():
    line_board = font.render("lines: " + str(levels), True, "green")
    score_board = font.render("Score: " + str(scores), True, "green")
    line_rect = line_board.get_rect()
    score_rect = score_board.get_rect()
    line_rect.center = (500, 650)
    score_rect.center = (150, 650)
    window.blit(line_board, line_rect)
    window.blit(score_board, score_rect)
    draw_tetris_board()
    draw_piece(current_one, x, y)
    pygame.draw.lines(window, (255, 0, 0), False,
                      [(start_x - 5, start_y), (start_x - 5, last_y + width + 5),
                       (585, last_y + width + 5), (585, start_y)], 5)


def calc_max_x(piece, x_pos):
    shape, _ = piece
    max_x = x_temp = x_pos
    for i in shape:
        done = False
        for j in i:
            if not done or (j and done):
                x_pos += width
                if j:
                    done = True
            if not j and done:
                break
        max_x = max(max_x, x_pos)
        x_pos = x_temp
    return max_x


def calc_max_y(piece, y_pos):
    return y_pos + (len(piece[0]) - 1) * height


def calc_xx_yy(x_pos, y_pos=0):
    return int((x_pos - start_x) / width), round((int(y_pos) - start_y) / height)


def save_piece(piece, x_ind, y_ind, y_pos):
    shape, color = piece
    y_max = y_pos + (len(shape) - 1) * height
    temp_xx = x_ind
    _, max_yy = calc_xx_yy(0, y_max)
    for i in current_one[0]:
        for j in i:
            if j:
                board[x_ind, y_ind] = 1
                color_board[x_ind, y_ind] = current_one[1]
            x_ind += 1
        y_ind += 1
        x_ind = temp_xx


SHAPES = [
    np.array([[0, 1, 0], [1, 1, 1]]),   # T
    np.array([[1, 1, 1, 1]]),   # I
    np.array([[1, 1], [1, 1]]),   # o
    np.array([[0, 1, 1], [1, 1, 0]]),   # S
    np.array([[1, 1, 0], [0, 1, 1]]),   # z
    np.array([[0, 0, 1], [1, 1, 1]]),   # L
    np.array([[1, 0, 0], [1, 1, 1]]),   # mirror of L
]
COLORS = [(128, 0, 128), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 130, 0), (0, 0, 255)]
scores = 0
levels = 0
board = np.zeros((10, 10), dtype=int)
color_board = np.empty((10, 10), dtype=tuple)
pygame.init()
window = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Tetris Game")
path = pathlib.Path(__file__).parent.resolve() / "soccer-scoreboard-font" / "SoccerScoreboard-XmMg.ttf"
font = pygame.font.Font(path, 40)
running = True
start_x = 120
last_x = 534
start_y = 140
last_y = 554
width = height = 46
y = 100.0
x = start_x + width * 4
rand = random.randint(0, 6)
current_one = (SHAPES[rand], COLORS[rand])
clock = pygame.time.Clock()
while running:
    xx, yy = calc_xx_yy(x, y)   # getting the index in the board
    max_y = calc_max_y(current_one, y)   # getting the max y in the shape
    running, x, y, scores, current_one = check_events(x, y, scores, current_one)   # the events

    if not check_collision(xx, yy, current_one) and max_y < last_y:   # checking if the object collide with another one
        y += 1
    else:
        save_piece(current_one, xx, yy, y)
        y = 100
        x = start_x + width * 4
        scores += 5
        rand = random.randint(0, 6)
        rotation = 0
        current_one = [SHAPES[rand], COLORS[rand]]

    board, scores, levels = check_done_rows(board, scores, levels)
    window.fill((0, 0, 0))
    drawing_stuff()
    pygame.display.update()
    clock.tick(60)
pygame.quit()

import pathlib
import random

import pygame as pygame
import numpy as np

GRID_BOARD = np.zeros((20, 10), dtype=int)
COLOR_BOARD = np.empty((20, 10), dtype=tuple)
SHAPES = [
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
]
COLORS = [(128, 0, 128), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 130, 0), (0, 0, 255)]
WIDTH = HEIGHT = 35
START_X = 80
START_Y = 80
END_X = START_X + (10 * WIDTH)
END_Y = START_Y + (20 * HEIGHT)


def draw_the_board():   # to draw the grid
    pygame.draw.lines(WINDOW, "red", True, [(START_X, START_Y), (START_X, END_Y), (END_X, END_Y), (END_X, START_Y)], 5)
    for col in range(1, 10):
        pygame.draw.line(WINDOW, "white", (START_X + (col * WIDTH), START_Y), (START_X + (col * WIDTH), END_Y))
    for row in range(1, 20):
        pygame.draw.line(WINDOW, "white", (START_X, START_Y + (row * HEIGHT)), (END_X, START_Y + (row * HEIGHT)))
    for row in range(0, 20):
        for col in range(0, 10):
            if GRID_BOARD[row][col]:
                pygame.draw.rect(WINDOW, COLOR_BOARD[row][col],
                                 [START_X + col * WIDTH, START_Y + row * HEIGHT, WIDTH, HEIGHT])


def show_credits():
    font1.bold = True
    credit_text1 = font1.render("Tetris Project", True, (255, 255, 255))
    font1.bold = False
    strings = ["This project is made by Mina Selim", "This project is made by Python",
               "This project is made by Pygame framework"]
    start = 1
    pos = 50
    for string in strings:
        credit_text = font1.render(string, True, (255, 255, 255))
        WINDOW.blit(credit_text, (50, pos + (start * 75)))
        start += 1
    WINDOW.blit(credit_text1, (300, 50))


def draw_tetris(piece, pos_x, pos_y):
    shape, color = piece
    temp_x = pos_x
    for i in shape:
        pos_x = temp_x
        for j in i:
            if j:
                pygame.draw.rect(WINDOW, color, [pos_x, pos_y, WIDTH, HEIGHT])
            pos_x += WIDTH
        pos_y += HEIGHT


def draw_stuff():
    draw_tetris(piece2, 550, 550)
    strings = ["Scores: ", "Lines: ", "Next: "]
    start = 0
    for string in strings:
        text = game_font.render(string, True, (0, 255, 0))
        rect = text.get_rect()
        rect.center = (600, 200 + (150 * start))
        start += 1
        WINDOW.blit(text, rect)
    var = [str(SCORES), str(LEVELS)]
    start = 0
    for v in var:
        text = game_font.render(v, True, (0, 255, 0))
        rect = text.get_rect()
        rect.center = (610, 260 + (150 * start))
        start += 1
        WINDOW.blit(text, rect)
    pygame.draw.circle(WINDOW, (0, 0, 255), (40, 50), 20)
    WINDOW.blit(paused_sign, (33, 42))
    pygame.draw.circle(WINDOW, (0, 0, 255), (40, 100), 20)


def calc_max_x_y(piece, pos_x, pos_y):
    shape, _ = piece
    temp_x = max_xxx = pos_x
    for i in shape:
        done = False
        for j in i:
            if (j and done) or not done:
                pos_x += WIDTH
                if j:
                    done = True
            if not j and done:
                break
        max_xxx = max(max_xxx, pos_x)
        pos_x = temp_x
    return max_xxx, len(shape) * HEIGHT + pos_y


def calc_ind_x_y(pos_x, pos_y):
    return round((pos_x - START_X) / WIDTH), round((pos_y - START_Y) / HEIGHT)


def save_tetris(piece, pos_x, pos_y):
    shape, color = piece
    ind_x, ind_y = calc_ind_x_y(pos_x, pos_y)
    temp_x = ind_x
    for i in shape:
        ind_x = temp_x
        for j in i:
            if j:
                GRID_BOARD[ind_y][ind_x] = 1
                COLOR_BOARD[ind_y][ind_x] = color
            ind_x += 1
        ind_y += 1


def make_tetris():
    rand = random.randint(0, 6)
    return SHAPES[rand], COLORS[rand]


def initial_pos():
    return (START_X + END_X) / 2, -80


pygame.init()
WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tetris Game")
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 30)
path = pathlib.Path(__file__).parent.resolve() / 'soccer-scoreboard-font' / 'SoccerScoreboard-XmMg.ttf'
game_font = pygame.font.Font(path, 40)

start_text = font.render("Start", True, "red")
start_rect = start_text.get_rect()
start_rect.center = (400, 200)
start_rec = start_rect.inflate(10, 10)

credits_text = font.render("Credits", True, "red")
credits_rect = credits_text.get_rect()
credits_rect.center = (400, 350)
credits_rec = credits_rect.inflate(10, 10)

quit_text = font.render("Quit", True, "red")
quit_rect = quit_text.get_rect()
quit_rect.center = (400, 500)
quit_rec = quit_rect.inflate(10, 10)

circle = pygame.draw.circle(WINDOW, "blue", (40, 50), 20)
circle2 = pygame.draw.circle(WINDOW, (0, 0, 255), (40, 100), 20)

paused_text = font2.render("paused", True, (255, 255, 255))

font2.bold = True
paused_sign = font2.render("II", True, (255, 0, 0))

while running:
    start_game = False
    credit = False
    WINDOW.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit_rec.collidepoint(pygame.mouse.get_pos()):
                    running = False
                if start_rec.collidepoint(pygame.mouse.get_pos()):
                    start_game = True
                    break
                if credits_rec.collidepoint(pygame.mouse.get_pos()):
                    credit = True
                    break

    if credit:
        WINDOW.fill((0, 0, 0))
        pygame.display.update()
        clock.tick(60)
        while credit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    credit = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if circle.collidepoint(pygame.mouse.get_pos()):
                            credit = False
            show_credits()
            pygame.draw.circle(WINDOW, "blue", (40, 50), 20)
            pygame.display.update()
            clock.tick(60)

    elif start_game:
        SCORES = 0
        LEVELS = 0
        WINDOW.fill((0, 0, 0))
        piece1 = make_tetris()
        piece2 = make_tetris()
        x, y = initial_pos()
        pause = False
        while start_game:
            max_x, max_y = calc_max_x_y(piece1, x, y)
            xx, yy = calc_ind_x_y(x, y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_game = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if circle.collidepoint(pygame.mouse.get_pos()):
                            pause = True
                            WINDOW.blit(paused_text, (60, 42))
                            WINDOW.blit(paused_sign, (33, 42))
                            pygame.display.update()
                            clock.tick(60)
                            break
                        if circle2.collidepoint(pygame.mouse.get_pos()):
                            start_game = False
                            break
                if event.type == pygame.KEYDOWN:
                    max_xx, max_yy = calc_ind_x_y(max_x, max_y)
                    if event.key == pygame.K_RIGHT:
                        if max_x + WIDTH <= END_X:
                            x += WIDTH
                    if event.key == pygame.K_LEFT:
                        if x - WIDTH >= START_X:
                            if not GRID_BOARD[yy][xx - 1]:
                                x -= WIDTH
                    if event.key == pygame.K_SPACE:
                        new = np.rot90(piece1[0], 1, (1, 0)), piece1[1]
                        max_new_x, _ = calc_max_x_y(new, x, y)
                        if max_new_x <= END_X:
                            piece1 = new
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        start_game = False
                        running = False
                        pause = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if circle.collidepoint(pygame.mouse.get_pos()):
                                pause = False
                                WINDOW.fill((0, 0, 0))
                                draw_the_board()
                                draw_stuff()
                                pygame.display.update()
                                clock.tick(60)
                                break
                            if circle2.collidepoint(pygame.mouse.get_pos()):
                                pause = False
                                start_game = False
                                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                y += 1
            WINDOW.fill((0, 0, 0))
            y += 1
            draw_the_board()
            draw_stuff()
            draw_tetris(piece1, x, y)
            if max_y >= END_Y:
                save_tetris(piece1, x, y)
                piece1 = piece2
                piece2 = make_tetris()
                x, y = initial_pos()

            pygame.display.update()
            clock.tick(60)
    else:
        pygame.draw.rect(WINDOW, "blue", start_rec)
        WINDOW.blit(start_text, start_rect)

        pygame.draw.rect(WINDOW, "blue", credits_rec)
        WINDOW.blit(credits_text, credits_rect)

        pygame.draw.rect(WINDOW, "blue", quit_rec)
        WINDOW.blit(quit_text, quit_rect)

    pygame.display.update()
    clock.tick(60)
pygame.quit()

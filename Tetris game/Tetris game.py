import pygame as pygame
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
WIDTH = HEIGHT = 35
START_X = 80
START_Y = 80
END_X = START_X + (10 * WIDTH)
END_Y = START_Y + (20 * HEIGHT)


def draw_the_board():   # to draw the grid
    pygame.draw.lines(window, "red", True, [(START_X, START_Y), (START_X, END_Y), (END_X, END_Y), (END_X, START_Y)], 5)
    for col in range(1, 10):
        pygame.draw.line(window, "white", (START_X + (col * WIDTH), START_Y), (START_X + (col * WIDTH), END_Y))
    for row in range(1, 20):
        pygame.draw.line(window, "white", (START_X, START_Y + (row * HEIGHT)), (END_X, START_Y + (row * HEIGHT)))


def show_credits():
    font1.bold = True
    credit_text1 = font1.render("Credits:", True, (255, 255, 255))
    font1.bold = False
    credit_text2 = font1.render("This project is made by Mina Selim", True, (255, 255, 255))
    window.blit(credit_text1, (50, 50))
    window.blit(credit_text2, (50, 100))


pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tetris Game")
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)
font1 = pygame.font.Font(None, 50)

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

while running:
    start_game = False
    credit = False
    window.fill((0, 0, 0))
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
        window.fill((0, 0, 0))
        pygame.display.update()
        clock.tick(60)
        while credit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    credit = False
            show_credits()
            pygame.display.update()
            clock.tick(60)
    elif start_game:
        window.fill((0, 0, 0))

        draw_the_board()
        pygame.display.update()
        clock.tick(60)
        while start_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_game = False

    else:
        pygame.draw.rect(window, "blue", start_rec)
        window.blit(start_text, start_rect)

        pygame.draw.rect(window, "blue", credits_rec)
        window.blit(credits_text, credits_rect)

        pygame.draw.rect(window, "blue", quit_rec)
        window.blit(quit_text, quit_rect)

    pygame.display.update()
    clock.tick(60)
pygame.quit()

import pathlib
import random

from Settings import *


def check_down_collision(piece, x_index, y_index):
    shape, color = piece[1]['shape'], piece[1]['color']
    x_temp = x_index
    for i in shape:
        x_index = x_temp
        for j in i:
            if j:
                if y_index != 19:
                    if GRID_BOARD[y_index + 1][x_index]:
                        return True
            x_index += 1
        y_index += 1
    return False


def move_done(y_max):
    if y_max + SIZE <= END_Y:
        return SIZE
    return 0


def get_color(row, col):
    return NUMS_COLORS.get(GRID_BOARD[row][col], BLACK)


def get_grid_color(color):
    return COLORS_NUM.get(color, BLACK)


def draw_the_board():   # to draw the grid and the blocks
    pygame.draw.lines(WINDOW, RED, True, [(START_X, START_Y), (START_X, END_Y), (END_X, END_Y), (END_X, START_Y)], 5)
    for row in range(ROWS):
        pos_y = row * SIZE
        for col in range(COLUMNS):
            pos_x = col * SIZE
            if GRID_BOARD[row][col]:
                pygame.draw.rect(WINDOW, get_color(row, col), [START_X + pos_x, START_Y + pos_y, SIZE, SIZE])
            if col:
                pygame.draw.line(WINDOW, WHITE, (START_X + pos_x, START_Y), (START_X + pos_x, END_Y))
        if row:
            pygame.draw.line(WINDOW, WHITE, (START_X, START_Y + pos_y), (END_X, START_Y + pos_y))


def show_credits():
    font1.bold = True
    credit_text1 = font1.render("Tetris Project", True, WHITE)
    font1.bold = False
    strings = ["This project is made by Mina Selim", "This project is made by Python",
               "This project is made by Pygame framework"]
    start = 1
    pos = 50
    for string in strings:
        credit_text = font1.render(string, True, WHITE)
        WINDOW.blit(credit_text, (50, pos + (start * 75)))
        start += 1
    WINDOW.blit(credit_text1, (300, 50))


def draw_tetris(piece, pos_x, pos_y):
    shape, color = piece[1]['shape'], piece[1]['color']
    temp_x = pos_x
    for i in shape:
        pos_x = temp_x
        for j in i:
            if j:
                pygame.draw.rect(WINDOW, color, [pos_x, pos_y, SIZE, SIZE])
            pos_x += SIZE
        pos_y += SIZE


def draw_stuff():
    draw_tetris(piece2, 550, 550)
    draw_the_board()
    strings = ["Scores: ", "Lines: ", "Next: "]
    start = 0
    for string in strings:
        text = game_font.render(string, True, GREEN)
        rect = text.get_rect()
        rect.center = (600, 200 + (150 * start))
        start += 1
        WINDOW.blit(text, rect)
    var = [str(SCORES), str(LEVELS)]
    start = 0
    for v in var:
        text = game_font.render(v, True, GREEN)
        rect = text.get_rect()
        rect.center = (610, 260 + (150 * start))
        start += 1
        WINDOW.blit(text, rect)
    pygame.draw.circle(WINDOW, BLUE, (40, 50), 20)
    WINDOW.blit(paused_sign, (33, 42))
    pygame.draw.circle(WINDOW, BLUE, (40, 100), 20)


def calc_max_x_y(piece, pos_x, pos_y):
    shape = piece[1]['shape']
    temp_x = max_xxx = pos_x
    for i in shape:
        done = False
        for j in i:
            if (j and done) or not done:
                pos_x += SIZE
                if j:
                    done = True
            if not j and done:
                break
        max_xxx = max(max_xxx, pos_x)
        pos_x = temp_x
    return max_xxx, len(shape) * SIZE + pos_y


def calc_ind_x_y(pos_x, pos_y):
    return round((pos_x - START_X) / SIZE), round((pos_y - START_Y) / SIZE)


def save_tetris(piece, pos_x, pos_y):
    shape, color = piece[1]['shape'], piece[1]['color']
    ind_x, ind_y = calc_ind_x_y(pos_x, pos_y)
    temp_x = ind_x
    for i in shape:
        ind_x = temp_x
        for j in i:
            if j:
                GRID_BOARD[ind_y][ind_x] = get_grid_color(color)
            ind_x += 1
        ind_y += 1


def make_tetris():
    return random.choice(list(TETRIS.items()))


def initial_pos():
    return (START_X + END_X) / 2, START_Y - SIZE * 4


def exit_game():
    pygame.quit()
    exit()


pygame.init()
WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tetris Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 30)
path = pathlib.Path(__file__).parent.resolve() / 'soccer-scoreboard-font' / 'SoccerScoreboard-XmMg.ttf'
game_font = pygame.font.Font(path, 40)

start_text = font.render("Start", True, RED)
start_rect = start_text.get_rect()
start_rect.center = (400, 200)
start_rec = start_rect.inflate(10, 10)

credits_text = font.render("Credits", True, RED)
credits_rect = credits_text.get_rect()
credits_rect.center = (400, 350)
credits_rec = credits_rect.inflate(10, 10)

quit_text = font.render("Quit", True, RED)
quit_rect = quit_text.get_rect()
quit_rect.center = (400, 500)
quit_rec = quit_rect.inflate(10, 10)

circle = pygame.draw.circle(WINDOW, BLUE, (40, 50), 20)
circle2 = pygame.draw.circle(WINDOW, BLUE, (40, 100), 20)

paused_text = font2.render("paused", True, WHITE)

font2.bold = True
paused_sign = font2.render("II", True, RED)

while True:
    start_game = False
    credit = False
    WINDOW.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit_rec.collidepoint(pygame.mouse.get_pos()):
                    exit_game()
                if start_rec.collidepoint(pygame.mouse.get_pos()):
                    start_game = True
                    break
                if credits_rec.collidepoint(pygame.mouse.get_pos()):
                    credit = True
                    break

    if credit:
        WINDOW.fill(BLACK)
        pygame.display.update()
        while credit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if circle.collidepoint(pygame.mouse.get_pos()):
                            credit = False
            show_credits()
            pygame.draw.circle(WINDOW, BLUE, (40, 50), 20)
            pygame.display.update()
            clock.tick(60)

    elif start_game:
        SCORES = 0
        LEVELS = 0
        WINDOW.fill(BLACK)
        piece1 = make_tetris()
        piece2 = make_tetris()
        x, y = initial_pos()
        pause = False
        update = pygame.USEREVENT
        pygame.time.set_timer(update, 500)
        SPEED = 5
        while start_game:
            max_x, max_y = calc_max_x_y(piece1, x, y)
            xx, yy = calc_ind_x_y(x, y)
            max_xx, max_yy = calc_ind_x_y(max_x, max_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
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
                    if event.key == pygame.K_RIGHT:
                        if max_x + SIZE <= END_X:
                            x += SIZE
                    if event.key == pygame.K_LEFT:
                        if x - SIZE >= START_X:
                            if not GRID_BOARD[yy][xx - 1]:
                                x -= SIZE
                    if event.key == pygame.K_SPACE:
                        new_shape = np.rot90(piece1[1]['shape'], 1, (1, 0)).tolist()
                        new_piece = (piece1[0], {'shape': new_shape, 'color': piece1[1]['color']})
                        max_new_x, _ = calc_max_x_y(new_piece, x, y)
                        if max_new_x <= END_X:
                            piece1 = new_piece
                            _, max_y = calc_max_x_y(new_piece, x, y)
                if event.type == update:
                    if max_y < END_Y - SIZE:
                        if (max_y >= START_Y and not check_down_collision(piece1, xx, yy)) or max_y <= START_Y:
                            y += move_done(max_y)
                        else:
                            save_tetris(piece1, x, y)
                            piece1 = piece2
                            piece2 = make_tetris()
                            x, y = initial_pos()
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if circle.collidepoint(pygame.mouse.get_pos()):
                                pause = False
                                WINDOW.fill(BLACK)
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
                if (max_y >= START_Y and not check_down_collision(piece1, xx, yy)) or max_y <= START_Y:
                    y += move_done(max_y)
                else:
                    save_tetris(piece1, x, y)
                    piece1 = piece2
                    piece2 = make_tetris()
                    x, y = initial_pos()
            WINDOW.fill(BLACK)
            draw_stuff()
            draw_tetris(piece1, x, y)
            if max_y >= END_Y:
                save_tetris(piece1, x, y)
                piece1 = piece2
                piece2 = make_tetris()
                x, y = initial_pos()

            pygame.display.update()
            clock.tick(10)
    else:
        pygame.draw.rect(WINDOW, BLUE, start_rec)
        WINDOW.blit(start_text, start_rect)

        pygame.draw.rect(WINDOW, BLUE, credits_rec)
        WINDOW.blit(credits_text, credits_rect)

        pygame.draw.rect(WINDOW, BLUE, quit_rec)
        WINDOW.blit(quit_text, quit_rect)

    pygame.display.update()

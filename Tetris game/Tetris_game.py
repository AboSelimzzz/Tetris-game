import pygame

from Constants import *
from Game import Game
from Score import Score
from Preview import Preview


def read_scores():
    try:
        with open('highscores.txt', 'r') as file:
            return [int(line.strip()) for line in file]
    except FileNotFoundError:
        return []


def write_score(score, scores):
    scores.append(int(score))
    scores.sort(reverse=True)
    with open('highscores.txt', 'w') as file:
        for s in scores:
            file.write(f'{s}\n')


class Main:
    def __init__(self):
        self.display_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.screen.get_rect(topleft=(0, 0))
        self.next_shape = choice(list(TETROMINOES.keys()))
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()
        self.music = pygame.mixer.Sound(join('music', 'music.wav'))
        self.music.set_volume(0.05)
        self.music.play(-1)
        self.pause_circle = None
        self.home_circle = None
        self.continue_circle = None
        self.end_score = None

    def get_next_shape(self):
        n = self.next_shape
        self.next_shape = choice(list(TETROMINOES.keys()))
        return n

    def update_score(self, lines, level, score):
        self.score.level = level
        self.score.lines = lines
        self.score.score = score

    def display_options(self):
        pause_img = pygame.image.load(join('options', 'Pause.jpg')).convert_alpha()
        home_img = pygame.image.load(join('options', 'Home.jpg')).convert_alpha()

        images = [pause_img, home_img]

        for i, img in enumerate(images):
            x = GAME_WIDTH + 6 * WIDTH_PADDING + i * OTHER_BAR / 2
            y = HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2
            img = pygame.transform.scale(img, (40, 40))
            img_rect = img.get_rect(center=(x, y))
            r = math.sqrt(img_rect.width ** 2 + img_rect.height ** 2) / 2
            if i == 1:
                self.home_circle = pygame.draw.circle(self.display_screen, WHITE, (int(x), int(y)), int(r))
            elif i == 0:
                self.continue_circle = pygame.draw.circle(self.display_screen, WHITE, (int(x), int(y)), int(r))
                self.pause_circle = pygame.draw.circle(self.display_screen, WHITE, (int(x), int(y)), int(r))
            else:
                break
            self.display_screen.blit(img, img_rect)
            pygame.display.flip()

    def pause_game(self):
        continue_img = load(join('options', 'Continue.jpg')).convert_alpha()
        img = pygame.transform.scale(continue_img, (40, 40))
        x = GAME_WIDTH + 6 * WIDTH_PADDING
        y = HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2
        img_rect = img.get_rect(center=(x, y))
        r = math.sqrt(img_rect.width ** 2 + img_rect.height ** 2) / 2
        self.display_screen.blit(img, img_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.continue_circle.collidepoint(pos):
                            self.display_options()
                            return True
                        if self.home_circle.collidepoint(pos):
                            return False

    def show_game_over(self):
        self.music.stop()
        font = pygame.font.Font(None, 100)
        font.set_bold(True)
        text = font.render("GAME OVER", True, BLACK)
        w, h = text.get_size()
        temp_surface = pygame.Surface((w + 20 * 40, h + 1 * 40))
        temp_surface.fill(WHITE)
        temp_surface.blit(text, (400, 20))
        rect = text.get_rect(center=(0, WINDOW_HEIGHT / 2))
        self.display_screen.blit(temp_surface, rect)
        pygame.display.flip()
        write_score(self.end_score, read_scores())
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.home_circle.collidepoint(pos):
                            return False

    def run(self):
        self.display_options()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.home_circle.collidepoint(pos):
                        running = False
                        self.music.stop()
                        break
                    if self.pause_circle.collidepoint(pos) and self.end_score is None:
                        running = self.pause_game()
                        if not running:
                            self.music.stop()
                            break

            self.end_score = self.game.run()
            if self.end_score is None:
                self.preview.run(self.next_shape)
                self.score.run()
                self.display_screen.blit(self.display_screen, self.rect)
                pygame.display.flip()
            else:
                running = self.show_game_over()

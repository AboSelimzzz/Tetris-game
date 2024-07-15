from Constants import *
from Game import Game
from Score import Score
from Preview import Preview


def read_scores():
    try:
        with open('highscores.txt', 'r') as file:
            lines = []
            for _ in range(10):
                line = file.readline()
                if line:
                    lines.append(int(line))
                else:
                    break
            return lines
    except FileNotFoundError:
        return []


def write_score(score, scores):
    scores.append(score)
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
        y = HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2
        offset_x = GAME_WIDTH + 3 * WIDTH_PADDING
        self.home_circle = pygame.draw.circle(self.display_screen, WHITE, (offset_x + 2 * OTHER_BAR / 3, y), 28)
        self.continue_circle = pygame.draw.circle(self.display_screen, WHITE, (offset_x, y), 28)
        self.sound_circle = pygame.draw.circle(self.display_screen, WHITE, (offset_x + OTHER_BAR / 3, y), 28)
        self.end_score = None
        self.muted = False
        self.display_options()

    def get_next_shape(self):
        n = self.next_shape
        self.next_shape = choice(list(TETROMINOES.keys()))
        return n

    def update_score(self, lines, level, score):
        self.score.level = level
        self.score.lines = lines
        self.score.score = score

    def display_options(self):
        names = ['Pause.jpg', 'Sound.jpg', 'Home.jpg']
        if self.muted:
            names[1] = 'Mute.jpg'

        for i, name in enumerate(names):
            x = GAME_WIDTH + 3 * WIDTH_PADDING + i * OTHER_BAR / 3
            y = HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2
            self.show_pic(['options', name], x, y)

    def pause_game(self):
        self.show_pic(['options', 'Continue.jpg'],
                      GAME_WIDTH + 3 * WIDTH_PADDING,
                      HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.display_options()
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.continue_circle.collidepoint(pos):
                            self.display_options()
                            return True
                        if self.home_circle.collidepoint(pos):
                            return False
                        if self.sound_circle.collidepoint(pos):
                            if not self.muted:
                                self.mute_sound()
                            else:
                                self.make_sound()

    def show_pic(self, path, x, y):
        img = pygame.image.load(join(path[0], path[1])).convert_alpha()
        img = pygame.transform.scale(img, (40, 40))
        img_rect = img.get_rect(center=(x, y))
        self.display_screen.blit(img, img_rect)
        pygame.display.flip()

    def make_sound(self):
        self.music.play(-1)
        self.game.tetromino.music.set_volume(0.07)
        self.show_pic(['options', 'Sound.jpg'], GAME_WIDTH + 3 * WIDTH_PADDING + OTHER_BAR / 3,
                      HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2)
        self.muted = False
        self.game.sound = True

    def mute_sound(self):
        self.music.stop()
        self.game.tetromino.music.set_volume(0)
        self.show_pic(['options', 'Mute.jpg'],
                      GAME_WIDTH + 3 * WIDTH_PADDING + OTHER_BAR / 3,
                      HEIGHT_PADDING + PREVIEW_HEIGHT_FRACTION * GAME_HEIGHT + HEIGHT_PADDING / 2)
        self.muted = True
        self.game.sound = False

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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = self.pause_game()
                        if not running:
                            self.music.stop()
                            break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.home_circle.collidepoint(pos):
                        running = False
                        self.music.stop()
                        break
                    if self.continue_circle.collidepoint(pos) and self.end_score is None:
                        running = self.pause_game()
                        if not running:
                            self.music.stop()
                            break
                    if self.sound_circle.collidepoint(pos):
                        if not self.muted:
                            self.mute_sound()
                        else:
                            self.make_sound()

            self.end_score = self.game.run()
            if self.end_score is None:
                self.preview.run(self.next_shape)
                self.score.run()
                self.display_screen.blit(self.display_screen, self.rect)
                pygame.display.flip()
            else:
                running = self.show_game_over()

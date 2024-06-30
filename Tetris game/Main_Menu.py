from Constants import *
from Tetris_game import Main


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TETRIS GAME")
        self.start_rect = None
        self.credit_rect = None
        self.quit_rect = None
        self.high_rect = None
        self.texts = ['Start', 'High Scores', 'Credit', 'Quit']
        self.font = pygame.font.Font(None, 50)
        self.score_font = pygame.font.Font(join('font', 'font.ttf'), 30)

    def display_text(self):
        for i, text in enumerate(self.texts):
            x = self.screen.get_width() / 2
            y = self.screen.get_height() / 4 * i + self.screen.get_height() / 6
            text_surface = self.font.render(text, True, RED)
            text_rect = text_surface.get_rect(center=(x, y))
            if text == 'Start':
                self.start_rect = text_rect
            elif text == 'Credit':
                self.credit_rect = text_rect
            elif text == 'High Scores':
                self.high_rect = text_rect
            else:
                self.quit_rect = text_rect
            self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        text = self.score_font.render('HIGH SCORES', True, GREEN)
        rect = text.get_rect(center=(363, 100))
        self.screen.blit(text, rect)
        for i in range(7):
            pygame.draw.line(self.screen, WHITE, (25, i * 100 + 50), (750, i * 100 + 50), 5)
        pygame.draw.line(self.screen, WHITE, (400, 150), (400, 650), 5)
        for i in range(2):
            pygame.draw.line(self.screen, WHITE, (25 + i * 725, 50), (25 + i * 725, 650), 5)

        pygame.display.update()

    def show_high(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        with open('highscores.txt', 'r') as file:
            for i in range(10):
                line = file.readline()
                text = self.score_font.render(f'{i + 1}-  ' + str(line[:-1]), True, GREEN)
                if i < 5:
                    rect = text.get_rect(center=(182, i * 100 + 200))
                    self.screen.blit(text, rect)
                else:
                    rect = text.get_rect(center=(557, (i - 5) * 100 + 200))
                    self.screen.blit(text, rect)
                pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.start_rect.collidepoint(pos):
                            Main().run()
                        if self.quit_rect.collidepoint(pos):
                            pygame.quit()
                            exit()
                        if self.high_rect.collidepoint(pos):
                            self.show_high()
            self.screen.fill(BLACK)
            self.display_text()
            pygame.display.flip()


if __name__ == "__main__":
    MainMenu().run()


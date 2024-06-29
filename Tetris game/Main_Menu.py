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
        self.texts = ['Start', 'Credit', 'Quit']
        self.font = pygame.font.Font(None, 50)

    def display_text(self):
        for i, text in enumerate(self.texts):
            x = self.screen.get_width() / 2
            y = self.screen.get_height() / 3 * i + self.screen.get_height() / 6
            text_surface = self.font.render(text, True, RED)
            text_rect = text_surface.get_rect(center=(x, y))
            if text == 'Start':
                self.start_rect = text_rect
            elif text == 'Credit':
                self.credit_rect = text_rect
            else:
                self.quit_rect = text_rect
            self.screen.blit(text_surface, text_rect)

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
            self.screen.fill(BLACK)
            self.display_text()
            pygame.display.flip()


if __name__ == "__main__":
    MainMenu().run()


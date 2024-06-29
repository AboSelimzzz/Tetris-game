from Constants import *


class Score:
    def __init__(self):
        self.surface = pygame.Surface((OTHER_BAR, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - HEIGHT_PADDING))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - WIDTH_PADDING, WINDOW_HEIGHT - HEIGHT_PADDING))

        self.font = pygame.font.Font(join('font', 'font.ttf'), 30)

        self.inc_height = self.surface.get_height() / 3

        self.lines = 0
        self.score = 0
        self.level = 1

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, GREEN)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        for i, text in enumerate([('Score', self.score), ('level', self.level), ('lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = i * self.inc_height + self.inc_height / 2
            self.display_text((x, y), text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

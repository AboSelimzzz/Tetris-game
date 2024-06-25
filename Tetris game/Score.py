from Constants import *

class Score:
    def __init__(self):
        self.surface = pygame.Surface((OTHER_BAR, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - HEIGHT_PADDING))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - WIDTH_PADDING, WINDOW_HEIGHT - HEIGHT_PADDING))

    def blit(self):
        return self.display_surface.blit(self.surface, self.rect)
from Constants import *

class Preview:
    def __init__(self):
        self.surface = pygame.Surface((OTHER_BAR, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - WIDTH_PADDING, HEIGHT_PADDING))

    def run(self):
        self.display_surface.blit(self.surface, self.rect)
        
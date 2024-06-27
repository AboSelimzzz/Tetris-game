from Constants import *


class Preview:
    def __init__(self):
        self.surface = pygame.Surface((OTHER_BAR, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topright=(WINDOW_WIDTH - WIDTH_PADDING, HEIGHT_PADDING))

        self.surfaces = {shape: load(join('shapes', f'{shape}.png')).convert_alpha() for shape in TETROMINOES.keys()}

    def display_shapes(self, shape):
        shape_surface = self.surfaces[shape]
        rect = shape_surface.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))
        self.surface.blit(shape_surface, rect)

    def run(self, shape):
        self.surface.fill(GRAY)
        self.display_shapes(shape)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, WHITE, self.rect, 2, 2)

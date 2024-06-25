from Constants import *
from Game import Game
from Score import Score
from Preview import Preview

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TETRIS GAME")
game = Game()
score = Score()
preview = Preview()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(GRAY)
    game.run()
    score.blit()
    preview.run()
    score.surface.fill(RED)
    pygame.display.update()

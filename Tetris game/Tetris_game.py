from Constants import *
from Game import Game
from Score import Score
from Preview import Preview


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TETRIS GAME")
        self.next_shape = choice(list(TETROMINOES.keys()))
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def get_next_shape(self):
        n = self.next_shape
        self.next_shape = choice(list(TETROMINOES.keys()))
        return n

    def update_score(self, lines, level, score):
        self.score.level = level
        self.score.lines = lines
        self.score.score = score

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill(GRAY)
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shape)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()

import pygame

from Constants import *
from Timer import Timer


class Game:
    def __init__(self):
        # surface
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_screen = pygame.display.get_surface()

        # sprites
        self.sprites = pygame.sprite.Group()

        # grid
        self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

        # shape
        self.tetromino = Tetromino(random.choice(list(TETROMINOES.keys())), self.sprites, self.create_tet, self.grid)

        # timers
        self.Timers = {
            'vertical': Timer(UPDATE_TIMER_SPEED, True, self.move_down),
            'horizontal': Timer(UPDATE_TIMER_MOVE),
            'rotate': Timer(UPDATE_TOMER_ROTATE),
        }
        self.Timers['vertical'].activate()

    def create_tet(self):
        self.delete_rows()
        self.tetromino = Tetromino(random.choice(list(TETROMINOES.keys())), self.sprites, self.create_tet, self.grid)

    def timer_update(self):
        for timer in self.Timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.Timers['horizontal'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.Timers['horizontal'].activate()
            if keys[pygame.K_RIGHT]:
                self.Timers['horizontal'].activate()
                self.tetromino.move_horizontal(1)

        if not self.Timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.Timers['rotate'].activate()

    def delete_rows(self):
        del_rows = []
        for i, row in enumerate(self.grid):
            if all(row):
                del_rows.append(i)
        if del_rows:
            for del_row in del_rows:
                for block in self.grid[del_row]:
                    block.kill()
                for row in self.grid:
                    for block in row:
                        if block and block.pos.y < del_row:
                            block.pos.y += 1

            self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
            for block in self.sprites:
                self.grid[int(block.pos.y)][int(block.pos.x)] = block

    def draw_grid(self):
        for col in range(COLUMNS):
            x = col * SIZE
            pygame.draw.line(self.surface, WHITE, (x, 0), (x, self.surface.get_height()), 1)
        for row in range(ROWS):
            y = row * SIZE
            pygame.draw.line(self.surface, WHITE, (0, y), (self.surface.get_width(), y), 1)
        points = [(0, 0), (0, self.surface.get_height()), (self.surface.get_width(), self.surface.get_height()),
                  (self.surface.get_width(), 0)]
        pygame.draw.lines(self.surface, RED, True, points, 5)

    def run(self):
        self.surface.fill(BLACK)
        # update
        self.input()
        self.timer_update()
        self.sprites.update()

        # draw
        self.sprites.draw(self.surface)
        self.draw_grid()

        self.display_screen.blit(self.surface, (WIDTH_PADDING, HEIGHT_PADDING))


class Tetromino:
    def __init__(self, shape, group, create_tetromino, grid):
        self.block_pos = TETROMINOES[shape]['shape']
        self.color = TETROMINOES[shape]['color']
        self.shape = shape
        self.create_tetromino = create_tetromino
        # blocks that made the shape
        self.blocks = [Block(group, pos, self.color) for pos in self.block_pos]
        self.grid = grid

    # collisions
    def next_move_horizontal_collide(self, direction):
        tmp = [block.horizontal_collide(block.pos.x + direction, self.grid) for block in self.blocks]
        return True if any(tmp) else False

    def next_move_vertical_collide(self, direction):
        tmp = [block.vertical_collide(block.pos.y + direction, self.grid) for block in self.blocks]
        return True if any(tmp) else False

    # moving
    def move_down(self):
        if not self.next_move_vertical_collide(1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.grid[int(block.pos.y)][int(block.pos.x)] = block
            self.create_tetromino()

    def move_horizontal(self, direction):
        if not self.next_move_horizontal_collide(direction):
            for block in self.blocks:
                block.pos.x += direction

    def rotate(self):
        if self.shape != '0':
            pivot_pos = self.blocks[0].pos
            new_blocks_pos = [block.rotate(pivot_pos) for block in self.blocks]

            for pos in new_blocks_pos:
                if pos.x == 0 or pos.x >= COLUMNS:
                    return
                if pos.y > ROWS:
                    return
                if self.grid[int(pos.y)][int(pos.x)]:
                    return

            for i, block in enumerate(self.blocks):
                block.pos = new_blocks_pos[i]



class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, col):
        super().__init__(group)
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(col)
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * SIZE)
        self.col = col

    def update(self):
        self.rect.topleft = self.pos * SIZE

    def horizontal_collide(self, x, grid):
        if not 0 <= x < COLUMNS:
            return True
        if grid[int(self.pos.y)][int(x)]:
            return True

    def vertical_collide(self, y, grid):
        if y >= ROWS:
            return True
        if y >= 0 and grid[int(y)][int(self.pos.x)]:
            return True

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

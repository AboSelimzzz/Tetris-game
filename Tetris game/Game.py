from Constants import *


class Game:
    def __init__(self, get_next_shape, update_score):
        # surface
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_screen = pygame.display.get_surface()

        self.get_next_shape = get_next_shape

        # sprites
        self.sprites = pygame.sprite.Group()

        # grid
        self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

        # shape
        self.tetromino = Tetromino(choice(list(TETROMINOES.keys())), self.sprites, self.create_tet, self.grid)

        self.down_speed = UPDATE_TIMER_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.pressed = False
        # timers
        self.Timers = {
            'vertical': Timer(self.down_speed, True, self.move_down),
            'horizontal': Timer(UPDATE_TIMER_MOVE),
            'rotate': Timer(UPDATE_TOMER_ROTATE),
        }
        self.Timers['vertical'].activate()

        self.lines = 0
        self.level = 1
        self.score = 0

        self.update_score = update_score

    def calculate_score(self, lines):
        self.lines += lines
        self.score = SCORE_DATA[lines] * self.level

        if self.lines / 10 > self.level:
            self.level += 1
            self.down_speed *= 0.75
            self.Timers['vertical'].duration = self.down_speed
        self.update_score(self.lines, self.level, self.score)

    def create_tet(self):
        self.delete_rows()
        self.tetromino = Tetromino(self.get_next_shape(), self.sprites, self.create_tet, self.grid)

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
        if not self.pressed and keys[pygame.K_DOWN]:
            self.pressed = True
            self.Timers['vertical'].duration = self.down_speed_faster

        if self.pressed and not keys[pygame.K_DOWN]:
            self.pressed = False
            self.Timers['vertical'].duration = self.down_speed

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
            self.calculate_score(len(del_rows))

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

import pygame
import random
import math
from constants import top_score_classic, main_menu


def classic_tetris(leaders, nickname, music_on_checker, volume):
    global top_score_classic

    pygame.init()

    if music_on_checker == True:
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/music1.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
        pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
        pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
    else:
        pass


    # Настройки
    board_dim = (10, 20)
    block_size = 30
    screen_width = 500
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # функция для рисования плитки
    def draw_tile(color, pos, border=4, surface=screen):
        pygame.draw.rect(
            surface, color, pygame.Rect(pos.a, pos.b, block_size, block_size)
        )
        pygame.draw.rect(
            surface,
            (int(color[0] * 0.8), int(color[1] * 0.8), int(color[2] * 0.8)),  # Серый цвет
            pygame.Rect(
                pos.a + border,
                pos.b + border,
                block_size - border * 2,
                block_size - border * 2,
            ),
        )

    # Цвета
    colors = [
        (255, 100, 100),
        (100, 255, 100),
        (100, 100, 255),
        (255, 255, 100),
        (255, 100, 255),
        (100, 255, 255),
    ]

    background_color = (30, 30, 30)

    # Шрифты
    font = pygame.font.Font('./assets/font_main.ttf', 18)

    # Блоки
    block_types = [
        [[1, 1], [1, 1]],
        [[1, 1, 1], [1, 1, 1]],
        [[1, 1], [1, 1], [1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1], [0, 1], [0, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[0, 1], [0, 1], [1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 0], [1, 1], [1, 0]],
        [[0, 1], [1, 1], [0, 1]],
        [[0, 1, 0], [1, 1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]],
        [[1, 1, 1, 1, 1]],
        [[1], [1], [1], [1], [1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[1, 0], [1, 1], [0, 1]],
        [[0, 1], [1, 1], [1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
        [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
    ]

    class Block:
        def __init__(self, shape):
            self.shape = shape
            self.width = len(shape[0])
            self.height = len(shape)


    class Board:
        def __init__(self):
            self.grid = [[0 for _ in range(board_dim[0])] for _ in range(board_dim[1])]
            self.clearing_rows = []
            self.current_score = 0

        def can_place(self, block, pos):
            """Проверяет, можно ли разместить блок на поле."""
            for y in range(block.height):
                for x in range(block.width):
                    if block.shape[y][x]:
                        # Проверяем, не выходит ли блок за границы поля или не пересекается ли с другими блоками
                        if (
                            pos[0] + x < 0
                            or pos[0] + x >= board_dim[0]
                            or pos[1] + y >= board_dim[1]
                            or self.grid[pos[1] + y][pos[0] + x]
                        ):
                            return False
            return True

        def place(self, block, pos, color):
            """Размещает блок на поле."""
            if self.can_place(block, pos):
                for y in range(block.height):
                    for x in range(block.width):
                        if block.shape[y][x]:
                            # Устанавливаем блок на поле
                            self.grid[pos[1] + y][pos[0] + x] = color
                return True
            return False

        def clear_lines(self):
            """Очищает заполненные строки и возвращает количество очищенных строк."""
            lines_cleared = []
            for y in range(board_dim[1]):
                if all(self.grid[y]):
                    lines_cleared.append(y)
            if lines_cleared:
                # Удаляем строки и блоки падают вниз
                for y in sorted(lines_cleared, reverse=True):
                    del self.grid[y]
                    self.grid.insert(0, [0 for _ in range(board_dim[0])])
                # Блоки падают вниз
                for y in range(board_dim[1]):
                    for x in range(board_dim[0]):
                        if self.grid[y][x]:
                            self.grid[y][x] = (
                                (
                                    self.grid[y][x][0],
                                    self.grid[y][x][1],
                                    self.grid[y][x][2],
                                    255,
                                )
                                if len(self.grid[y][x]) == 4
                                else (*self.grid[y][x], 255)
                            )
                self.clearing_rows = lines_cleared
                return len(lines_cleared)
            return 0

        def update_clearing(self):
            """Обновляет состояние очистки строк."""
            if self.clearing_rows:
                # Блоки падают вниз
                for y in range(board_dim[1]):
                    for x in range(board_dim[0]):
                        if self.grid[y][x]:
                            self.grid[y][x] = (
                                (
                                    self.grid[y][x][0],
                                    self.grid[y][x][1],
                                    self.grid[y][x][2],
                                    max(0, self.grid[y][x][3] - 20),
                                )
                                if len(self.grid[y][x]) == 4
                                else (*self.grid[y][x], 255)
                            )
                # Проверяем, упали ли блоки вниз
                if all(
                    self.grid[y][x][3] == 0
                    for y in range(board_dim[1])
                    for x in range(board_dim[0])
                    if self.grid[y][x]
                ):
                    # Блоки упали вниз, обновляем поле
                    for y in range(board_dim[1]):
                        for x in range(board_dim[0]):
                            if self.grid[y][x]:
                                self.grid[y][x] = (
                                    (
                                        self.grid[y][x][0],
                                        self.grid[y][x][1],
                                        self.grid[y][x][2],
                                        255,
                                    )
                                    if len(self.grid[y][x]) == 4
                                    else (*self.grid[y][x], 255)
                                )
                    self.clearing_rows = []

        def draw(self):
            """Отрисовывает игровое поле."""
            for y in range(board_dim[1]):
                for x in range(board_dim[0]):
                    if self.grid[y][x]:
                        color = (
                            self.grid[y][x][:3]
                            if len(self.grid[y][x]) == 4
                            else self.grid[y][x]
                        )
                        alpha = self.grid[y][x][3] if len(self.grid[y][x]) == 4 else 255
                        surface = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
                        pygame.draw.rect(
                            surface, color + (alpha,), (0, 0, block_size, block_size)
                        )
                        screen.blit(surface, (50 + x * block_size, 50 + y * block_size))

    class SparkBox:
        def __init__(self):
            self.sparks = []

        def add(self, spark):
            self.sparks.append(spark)

        def update(self):
            to_remove = []
            for spark in self.sparks:
                spark.update()
                if spark.remove:
                    to_remove.append(spark)
            for spark in to_remove:
                self.sparks.remove(spark)

        def draw(self):
            for spark in self.sparks:
                spark.draw()


    class Spark:
        def __init__(self, pos, size):
            self.pos = pos
            self.size = size
            self.dir = random_vector()
            self.speed = random.randint(0, 10)
            self.remove = False

        def update(self):
            self.speed /= 1.1
            self.pos += self.dir * self.speed
            self.size /= 1.2
            if self.size < 0.1:
                self.remove = True

        def draw(self):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                pygame.Rect(self.pos.a, self.pos.b, self.size, self.size),
            )


    def random_vector():
        angle = math.tau * random.randint(0, 100) / 100
        return CoolPoint(math.sin(angle), math.cos(angle))


    class CoolPoint:
        def __init__(self, a, b):
            self.a = a
            self.b = b
            self.pair = (a, b)
            self.size = math.sqrt(a**2 + b**2)

        def make_small(self):
            if self.size == 0:
                return self.duplicate()
            return CoolPoint(self.a / self.size, self.b / self.size)

        def duplicate(self):
            return CoolPoint(self.a, self.b)

        def mix(self, other):
            return self.a * other.a + self.b * other.b

        def blend(self, other):
            return CoolPoint(self.a * other.a, self.b * other.b)

        def squeeze(self, low=(0, 0), high=(255, 255)):
            return CoolPoint(
                min(max(self.a, low[0]), high[0]), min(max(self.b, low[1]), high[1])
            )

        def change(self, a=None, b=None):
            if a is not None:
                self.a = a
            if b is not None:
                self.b = b

        def refresh(self):
            self.pair = (self.a, self.b)
            self.size = math.sqrt(self.a**2 + self.b**2)

        def __add__(self, other):
            return CoolPoint(self.a + other.a, self.b + other.b)

        def __sub__(self, other):
            return CoolPoint(self.a - other.a, self.b - other.b)

        def __mul__(self, num):
            return CoolPoint(self.a * num, self.b * num)

        def __truediv__(self, num):
            return CoolPoint(self.a / num, self.b / num)

        def __neg__(self):
            return CoolPoint(-self.a, -self.b)

        def __abs__(self):
            return CoolPoint(abs(self.a), abs(self.b))

        def __str__(self):
            return f"{self.a} {self.b}"

        def __mod__(self, num):
            return CoolPoint(self.a % num, self.b % num)

        def __floordiv__(self, num):
            return CoolPoint(self.a // num, self.b // num)

    # Цвета для переливания
    colors_gradient = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
    COLOR_CHANGE_INTERVAL = 500
    last_color_change_time = pygame.time.get_ticks()
    color_index = 0

    # Функция для отображения текста с переливанием
    def draw_text_with_gradient(text, font, surface, x, y):
        nonlocal last_color_change_time, color_index
        current_time = pygame.time.get_ticks()
        if current_time - last_color_change_time >= COLOR_CHANGE_INTERVAL:
            color_index = (color_index + 1) % len(colors_gradient)
            last_color_change_time = current_time
        color = colors_gradient[color_index]
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))

    class Game:
        def __init__(self):
            self.board = Board()
            self.block = Block(random.choice(block_types))
            self.block_pos = [board_dim[0] // 2 - self.block.width // 2, 0]  # Начальная позиция блока
            self.block_color = random.choice(colors)
            self.score = 0
            self.game_over = False
            self.hold_block = None
            self.can_hold = True
            self.next_block = Block(random.choice(block_types))
            self.next_block_color = random.choice(colors)
            self.spark_box = SparkBox()
            self.block_fall_speed = 0
            self.fall_interval = 40  # Начальная скорость падения

        def new_block(self):
            """Создает новый блок и проверяет, не закончилась ли игра."""
            self.block = self.next_block
            self.block_pos = [board_dim[0] // 2 - self.block.width // 2, 0]  # Центрируем новый блок
            self.block_color = self.next_block_color
            self.next_block = Block(random.choice(block_types))
            self.next_block_color = random.choice(colors)
            self.can_hold = True

            # Увеличиваем скорость падения, но не ниже минимального значения
            self.fall_interval = max(25, self.fall_interval - 5)

            # Проверяем, можно ли разместить новый блок
            if not self.board.can_place(self.block, self.block_pos):
                self.game_over = True

        def update(self):
            """Обновляет состояние игры."""
            if not self.game_over:
                self.block_fall_speed += 1
                if self.block_fall_speed >= self.fall_interval:
                    self.block_fall_speed = 0
                    # Проверяем, может ли блок упасть ниже
                    if not self.board.can_place(self.block, [self.block_pos[0], self.block_pos[1] + 1]):
                        # Если блок не может упасть ниже, размещаем его на поле
                        self.board.place(self.block, self.block_pos, self.block_color)
                        lines_cleared = self.board.clear_lines()
                        self.score += lines_cleared * 100  # Увеличиваем счет
                        self.board.update_clearing()
                        self.spark_box.update()
                        self.new_block()  # Создаем новый блок
                    else:
                        # Если блок может упасть ниже, перемещаем его вниз
                        self.block_pos[1] += 1
                self.board.update_clearing()

        def draw(self):
            """Отрисовывает игровое поле, блоки и интерфейс."""
            # Отрисовка рамки игрового поля
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                pygame.Rect(50, 50, board_dim[0] * block_size, board_dim[1] * block_size),
                1,
            )

            # Отрисовка игрового поля
            self.board.draw()

            # Отрисовка текущего блока
            for y in range(self.block.height):
                for x in range(self.block.width):
                    if self.block.shape[y][x]:
                        draw_tile(
                            self.block_color,
                            CoolPoint(
                                50 + (self.block_pos[0] + x) * block_size,
                                50 + (self.block_pos[1] + y) * block_size,
                            ),
                            border=2,
                            surface=screen,
                        )

            # Отрисовка счета и лучшего результата
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (350, 50))

            best_text = font.render(f"Best: {top_score_classic}", True, (255, 255, 255))
            screen.blit(best_text, (350, 100))

            # Отрисовка следующего блока
            next_block_text = font.render("Next Block:", True, (255, 255, 255))
            screen.blit(next_block_text, (350, 150))

            for y in range(self.next_block.height):
                for x in range(self.next_block.width):
                    if self.next_block.shape[y][x]:
                        draw_tile(
                            self.next_block_color,
                            CoolPoint(370 + x * block_size, 200 + y * block_size),
                            border=2,
                            surface=screen,
                        )

            # Отрисовка эффектов (искры)
            self.spark_box.draw()

            # Отрисовка "Game Over", если игра закончена
            if self.game_over:
                draw_text_with_gradient("GAME OVER!", font, screen, 125, 280)
                draw_text_with_gradient("Вернитесь в меню", font, screen, 75, 300)
                draw_text_with_gradient("или начните игру заново", font, screen, 35, 320)

    game = Game()

    running = True
    while running:

        screen.fill(background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.block_pos[0] -= 1
                    if not game.board.can_place(game.block, game.block_pos):
                        game.block_pos[0] += 1
                if event.key == pygame.K_RIGHT:
                    game.block_pos[0] += 1
                    if not game.board.can_place(game.block, game.block_pos):
                        game.block_pos[0] -= 1
                if event.key == pygame.K_DOWN:
                    game.block_pos[1] += 1
                    if not game.board.can_place(game.block, game.block_pos):
                        game.block_pos[1] -= 1
                if event.key == pygame.K_UP:
                    rotated_block = Block(
                        [list(row) for row in zip(*game.block.shape[::-1])]
                    )
                    if game.board.can_place(rotated_block, game.block_pos):
                        game.block = rotated_block
                if event.key == pygame.K_ESCAPE:
                    if music_on_checker == True:
                        pygame.mixer.init()
                        pygame.mixer.music.load("./assets/music.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
                        pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
                        pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
                    else:
                        pass
                    return

                if event.key == pygame.K_MINUS:
                    # Уменьшение громкости
                    volume = max(0.0, volume - 0.1)  # Уменьшаем громкость на 10%
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_EQUALS:
                    # Увеличение громкости
                    if volume > 1.0:
                        volume = 1.0
                    volume = min(1.0, volume + 0.1)  # Увеличиваем громкость на 10%
                    pygame.mixer.music.set_volume(volume)

        game.update()
        game.draw()

        if game.game_over:
            if game.score > top_score_classic:
                top_score_classic = game.score
            if nickname not in leaders:
                leaders[nickname] = [0, 0, 0]
            if top_score_classic > leaders[nickname][0]:
                leaders[nickname][0] = top_score_classic
            if pygame.mouse.get_pressed()[0]:
                game = Game()

        pygame.display.flip()
        clock.tick(60)


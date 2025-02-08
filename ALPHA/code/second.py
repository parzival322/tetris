import pygame
import random
import math
from constants import top_score_modern, main_menu


def modern_tetris(leaders, nickname, music_on_checker, volume):
    global top_score_modern

    pygame.init()

    if music_on_checker == True:
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/music2.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
        pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
        pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
    else:
        pass

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

    # класс для частиц (эффекты при удалении строк)
    class Spark:
        def __init__(self, pos, size):
            self.pos = pos  # позиция частицы
            self.size = size  # размер частицы
            self.dir = random_vector()  # направление движения
            self.speed = random.randint(0, 10)  # скорость
            self.remove = False  # флаг для удаления

        def update(self):
            self.speed /= 1.1  # замедляем частицу
            self.pos += self.dir * self.speed  # двигаем частицу
            self.size /= 1.2  # уменьшаем размер
            if self.size < 0.1:  # если частица слишком маленькая, удаляем
                self.remove = True

        def draw(self):
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                pygame.Rect(self.pos.a, self.pos.b, self.size, self.size),
            )

    # контейнер для частиц
    class SparkBox:
        def __init__(self):
            self.sparks = []  # список частиц

        def add(self, spark):
            self.sparks.append(spark)  # добавляем частицу

        def update(self):
            to_remove = []  # частицы для удаления
            for spark in self.sparks:
                spark.update()  # обновляем каждую частицу
                if spark.remove:
                    to_remove.append(spark)  # добавляем в список на удаление
            for spark in to_remove:
                self.sparks.remove(spark)  # удаляем частицы

        def draw(self):
            for spark in self.sparks:
                spark.draw()  # рисуем каждую частицу

    # класс для игрового поля
    class GameBoard:
        def __init__(self, size, current_score=0):
            self.size = size  # размер поля
            self.current_score = current_score
            self.grid = [
                [0 for _ in range(self.size.a)] for _ in range(self.size.b)
            ]  # сетка поля
            self.colors = [
                [SuperPoint(0, 0, 0) for _ in range(self.size.a)]
                for _ in range(self.size.b)
            ]  # цвета блоков

        def is_inside(self, pos):
            return (
                pos.a >= 0
                and pos.a < self.size.a
                and pos.b >= 0
                and pos.b < self.size.b
            )  # проверка, внутри ли поля

        def reset(self):
            self.grid = [
                [0 for _ in range(self.size.a)] for _ in range(self.size.b)
            ]  # сброс поля

        def can_place(self, block, pos):
            for y in range(len(block.shape)):
                for x in range(len(block.shape[y])):
                    if block.shape[y][x] == 1:
                        global_pos = pos + CoolPoint(x, y)  # глобальная позиция
                        if (
                            not self.is_inside(global_pos)
                            or self.grid[global_pos.b][global_pos.a] == 1
                        ):
                            return False  # нельзя поставить блок
            return True  # можно поставить блок

        def place(self, block, color, pos):
            if self.can_place(block, pos):
                for y in range(len(block.shape)):
                    for x in range(len(block.shape[y])):
                        if block.shape[y][x] == 1:
                            self.grid[pos.b + y][pos.a + x] = 1  # ставим блок
                            self.colors[pos.b + y][pos.a + x] = color  # задаем цвет
                return True
            return False

        def draw(self):
            screen.blit(background, (0, 0))  # рисуем фон
            for y in range(self.size.b):
                for x in range(self.size.a):
                    if self.grid[y][x] == 1:
                        draw_tile(
                            self.colors[y][x], CoolPoint(x, y) * tile_size
                        )  # рисуем плитку

        def clear_lines(self):
            rows_to_clear = []  # строки для очистки
            cols_to_clear = []  # столбцы для очистки

            # проверка строк
            for y in range(self.size.b):
                if sum(self.grid[y]) == self.size.a:
                    rows_to_clear.append(y)

            # проверка столбцов
            for x in range(self.size.a):
                total = 0
                for y in range(self.size.b):
                    total += self.grid[y][x]
                if total == self.size.b:
                    cols_to_clear.append(x)

            # очистка строк
            for row in rows_to_clear:
                self.grid[row] = [0 for _ in range(self.size.a)]
                for x in range(self.size.a):
                    spark_box.add(
                        Spark(
                            CoolPoint(x, row) * tile_size
                            + CoolPoint(tile_size, tile_size) * 0.5,
                            random.randint(0, 50),
                        )
                    )

            # очистка столбцов
            for col in cols_to_clear:
                for y in range(self.size.b):
                    self.grid[y][col] = 0
                    spark_box.add(
                        Spark(
                            CoolPoint(col, y) * tile_size
                            + CoolPoint(tile_size, tile_size) * 0.5,
                            random.randint(0, 50),
                        )
                    )

            self.current_score += score_values[
                len(rows_to_clear) + len(cols_to_clear)
            ]  # обновляем счет

        def is_game_over(self, draggable_blocks):
            for draggable_block in draggable_blocks:  # перебираем DraggableBlock
                block = draggable_block.block  # получаем Block из DraggableBlock
                for y in range(self.size.b):
                    for x in range(self.size.a):
                        if self.can_place(block, CoolPoint(x, y)):  # проверяем Block
                            return False  # игра не окончена
            return True  # игра окончена

    # класс для блока
    class Block:
        def __init__(self, shape):
            self.shape = shape  # форма блока
            self.width = len(self.shape[0])  # ширина
            self.height = len(self.shape)  # высота

    # класс для перемещаемого блока
    class DraggableBlock:
        def __init__(self, block, start_pos, board):
            self.block = block  # блок
            self.pos = start_pos  # начальная позиция
            self.valid_pos = start_pos  # валидная позиция
            self.color = random.choice(colors)  # случайный цвет
            self.board = board  # ссылка на игровое поле

        def draw(self, current_block, mouse_pos):
            if current_block != self:
                temp_surface = pygame.Surface((500, 500), pygame.SRCALPHA)
                for y in range(len(self.block.shape)):
                    for x in range(len(self.block.shape[y])):
                        if self.block.shape[y][x] == 1:
                            draw_tile(
                                self.color,
                                CoolPoint(x, y) * tile_size,
                                surface=temp_surface,
                            )
                scaled_surface = pygame.transform.scale_by(temp_surface, 0.5)
                screen.blit(scaled_surface, self.pos.pair)
                return

            can_fit = True
            if mouse_pos.b + (
                len(self.block.shape) - 1
            ) * tile_size >= game_size.b * tile_size or self.board.can_place(
                self.block, mouse_pos // tile_size
            ):
                self.valid_pos = mouse_pos
                can_fit = False

            for y in range(len(self.block.shape)):
                for x in range(len(self.block.shape[y])):
                    if self.block.shape[y][x] == 1:
                        tile_pos = mouse_pos + CoolPoint(x, y) * tile_size
                        if (
                            mouse_pos.b + (len(self.block.shape) - 1) * tile_size
                            < game_size.b * tile_size
                            and not can_fit
                        ):
                            draw_tile(self.color, tile_pos // tile_size * tile_size)
                        else:
                            draw_tile(self.color, tile_pos)

        def is_hovered(self, mouse_pos):
            scale = 0.5
            return (
                mouse_pos.a > self.pos.a
                and mouse_pos.a
                < self.pos.a + len(self.block.shape[0]) * tile_size * scale
                and mouse_pos.b > self.pos.b
                and mouse_pos.b < self.pos.b + len(self.block.shape) * tile_size * scale
            )

    # класс для 3d точки (вектора)
    class SuperPoint:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
            self.trio = (x, y, z)
            self.size = math.sqrt(x**2 + y**2 + z**2)

        def make_small(self):
            if self.size == 0:
                return self.duplicate()
            return SuperPoint(
                self.x / self.size, self.y / self.size, self.z / self.size
            )

        def duplicate(self):
            return SuperPoint(self.x, self.y, self.z)

        def mix(self, other):
            return self.x * other.x + self.y * other.y + self.z * other.z

        def blend(self, other):
            return SuperPoint(self.x * other.x, self.y * other.y, self.z * other.z)

        def squeeze(self, low=(0, 0, 0), high=(255, 255, 255)):
            return SuperPoint(
                min(max(self.x, low[0]), high[0]),
                min(max(self.y, low[1]), high[1]),
                min(max(self.z, low[2]), high[2]),
            )

        def change(self, x=None, y=None, z=None):
            if x is not None:
                self.x = x
            if y is not None:
                self.y = y
            if z is not None:
                self.z = z

        def refresh(self):
            self.trio = (self.x, self.y, self.z)
            self.size = math.sqrt(self.x**2 + self.y**2 + self.z**2)

        def __add__(self, other):
            return SuperPoint(self.x + other.x, self.y + other.y, self.z + other.z)

        def __sub__(self, other):
            return SuperPoint(self.x - other.x, self.y - other.y, self.z - other.z)

        def __mul__(self, num):
            return SuperPoint(self.x * num, self.y * num, self.z * num)

        def __truediv__(self, num):
            return SuperPoint(self.x / num, self.y / num, self.z / num)

        def __neg__(self):
            return SuperPoint(-self.x, -self.y, -self.z)

        def __abs__(self):
            return SuperPoint(abs(self.x), abs(self.y), abs(self.z))

        def __str__(self):
            return f"{self.x} {self.y} {self.z}"

    # класс для 2d точки (вектора)
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

    # функция для создания случайного вектора
    def random_vector():
        angle = math.tau * random.randint(0, 100) / 100
        return CoolPoint(math.sin(angle), math.cos(angle))

    game_size = CoolPoint(10, 10)  # размеры игрового поля
    tile_size = 50  # размер плитки

    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((500, 650))
    clock = pygame.time.Clock()

    # массивы для очков и цветов
    score_values = (0, 100, 250, 400, 800, 2000, 3000, 4000, 5000, 6000)
    colors = (
        SuperPoint(255, 100, 100),
        SuperPoint(100, 255, 100),
        SuperPoint(100, 100, 255),
        SuperPoint(255, 255, 100),
        SuperPoint(255, 100, 255),
        SuperPoint(100, 255, 255),
    )

    # функция для рисования плитки
    def draw_tile(color, pos, border=4, surface=screen):
        pygame.draw.rect(
            surface, color.trio, pygame.Rect(pos.a, pos.b, tile_size, tile_size)
        )
        pygame.draw.rect(
            surface,
            (color * 0.8).trio,
            pygame.Rect(
                pos.a + border,
                pos.b + border,
                tile_size - border * 2,
                tile_size - border * 2,
            ),
        )

    # функция для рисования фона
    def create_background():
        background = pygame.Surface((game_size * tile_size).pair)
        for x in range(game_size.a):
            for y in range(game_size.b):
                draw_tile(
                    SuperPoint(20, 20, 20),
                    CoolPoint(x, y) * tile_size,
                    surface=background,
                )
        return background

    # создаем контейнер для частиц
    spark_box = SparkBox()

    # создаем игровое поле
    board = GameBoard(game_size, 0)
    modern_score = board.current_score

    # создаем фон
    background = create_background()

    # массив всех возможных форм блоков
    block_shapes = [
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

    # создание блоков
    blocks = [Block(shape) for shape in block_shapes]

    # текущий блок
    current_block = None

    # массив выбора блоков
    block_choices = [
        DraggableBlock(
            random.choice(blocks),
            CoolPoint(
                game_size.a / 3 * i * tile_size + 50, game_size.b * tile_size + 50
            ),
            board,
        )
        for i in range(3)
    ]

    # шрифты
    font = pygame.font.Font("./assets/font_main.ttf", 25)
    small_font = pygame.font.Font("./assets/font_main.ttf", 15)
    big_font = pygame.font.Font("./assets/font_main.ttf", 50)

    # флаг проигрыша
    game_over = False
    running = True
    # основной цикл
    while running:
        modern_score = board.current_score

        keys = pygame.key.get_pressed()
        mouse_pos = CoolPoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
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

        if keys[pygame.K_ESCAPE]:
            if music_on_checker == True:
                pygame.mixer.init()
                pygame.mixer.music.load("./assets/music.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
                pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
                volume = 0.5  # Начальная громкость (50%)
                pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
            else:
                pass
            running = False

        screen.fill((30, 30, 30))

        if not game_over:
            if pygame.mouse.get_pressed()[0]:
                for block in block_choices:
                    if block.is_hovered(mouse_pos):
                        current_block = block
                        break
            else:
                if current_block is not None:
                    can_place = board.place(
                        current_block.block,
                        current_block.color,
                        current_block.valid_pos // tile_size,
                    )
                    if can_place:
                        block_choices.remove(current_block)
                current_block = None

            board.clear_lines()

            if len(block_choices) == 0:
                block_choices = [
                    DraggableBlock(
                        random.choice(blocks),
                        CoolPoint(
                            game_size.a / 3 * i * tile_size + 50,
                            game_size.b * tile_size + 50,
                        ),
                        board,
                    )
                    for i in range(3)
                ]

            if board.is_game_over(block_choices):
                game_over = True

            spark_box.update()

        board.draw()
        for block in block_choices:
            block.draw(current_block, mouse_pos)

        spark_box.draw()

        score_text = font.render(f"Score: {modern_score}", 1, (255, 255, 255))
        best_text = small_font.render(f"Best: {top_score_modern}", 1, (255, 255, 255))

        if not game_over:
            screen.blit(score_text, (0, 500))
            screen.blit(best_text, (0, 525))
        else:
            if modern_score > top_score_modern:
                top_score_modern = modern_score

            draw_text_with_gradient("GAME OVER!", big_font, screen, 65, 220)
            draw_text_with_gradient(f"Score: {modern_score} Best: {top_score_modern}", font, screen, 55, 280)


            if nickname not in leaders:
                leaders[nickname] = [0, 0, 0]
            if top_score_modern > leaders[nickname][1]:
                leaders[nickname][1] = top_score_modern

            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                game_over = False
                block_choices = [
                    DraggableBlock(
                        random.choice(blocks),
                        CoolPoint(
                            game_size.a / 3 * i * tile_size + 50,
                            game_size.b * tile_size + 50,
                        ),
                        board,
                    )
                    for i in range(3)
                ]
                current_block = None
                board.reset()
                board.current_score = 0

        pygame.display.flip()
        clock.tick(60)
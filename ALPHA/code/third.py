import pygame
import random
import math
import os
from constants import new_data_counter, top_score_genius, main_menu


def genius_mode(leaders, nickname, music_on_checker, volume):
    global top_score_genius, new_data_counter

    pygame.init()

    def load_images_from_folder(folder):
        images = []
        for filename in os.listdir(folder):
            img = pygame.image.load(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
        return images

    # Загрузка изображений
    images = load_images_from_folder("./assets/pictures")

    if music_on_checker == True:
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/music3.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
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

    pygame.mouse.set_visible(False)  # отключаем стандартный курсор
    try:
        cursor_image = pygame.image.load('./assets/cursor_genius.png')
        cursor_image = pygame.transform.scale(cursor_image, (32, 32))
        cursor_image.set_colorkey((255, 255, 255))  # указываем белый цвет как прозрачный фон
    except FileNotFoundError:
        print("Файл cursor_genius.png не найден. Используется стандартный курсор.")
        return

    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 650
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Цвета
    WHITE = (255, 255, 255)
    RED = (255,0,0)
    BLACK = (0, 0, 0)

    # Настройки игры
    BLOCK_SIZE = 50
    FALL_SPEED = 5
    SPAWN_RATE = 25  # Чем меньше, тем чаще появляются блоки
    LEVEL_UP_SCORE = 10  # Очков для перехода на следующий уровень

    # Шрифт
    font = pygame.font.Font('./assets/font_main.ttf', 36)
    
    # Класс блока
    class BlockBlast:
        def __init__(self, x, y, image):
            self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            self.image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))

        def draw(self):
            screen.blit(self.image, self.rect)

        def move(self):
            self.rect.y += FALL_SPEED

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

    # Основная функция игры
    clock = pygame.time.Clock()
    running = True
    score = 0
    level = 1
    blocks = []
    game_over = False

    while running:
        screen.fill((30, 30, 30))  # цвет фона
        mouse_pos = pygame.mouse.get_pos()

        # Генерация новых блоков
        if not game_over and random.randint(1, SPAWN_RATE) == 1:
            x = random.randint(0, 450)
            image = random.choice(images)
            blocks.append(BlockBlast(x, 0, image))

        # Отрисовываем падающие картинки
        for block in blocks[:]:
            block.move()
            block.draw()
            if block.rect.y > 650:
                game_over = True

        # Обработка кликов
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                for block in blocks[:]:
                    if block.is_clicked(pos):
                        blocks.remove(block)
                        score += 1
                        if score % LEVEL_UP_SCORE == 0:
                            FALL_SPEED += 1  # Увеличиваем скорость падения
                        if score % 10 == 0:
                            level += 1  # Увеличива-м уровень
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if music_on_checker == True:
                        pygame.mixer.init()
                        pygame.mixer.music.load("./assets/music.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
                        pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
                        pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость
                    else:
                        pass
                    running = False
                    pygame.mouse.set_visible(True)
                    return  # выход по кнопке ESCAPE
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



        # Отрисовываем курсор
        screen.blit(cursor_image, (mouse_pos[0] - cursor_image.get_width() // 2, mouse_pos[1] - cursor_image.get_height() // 2))

        # Отображение счета и уровня
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Отображение Game Over
        if game_over:
            if score > top_score_genius:
                top_score_genius = score
            if nickname not in leaders:
                leaders[nickname] = [0, 0, 0]
            if top_score_genius > leaders[nickname][2]:
                leaders[nickname][2] = top_score_genius
            

            draw_text_with_gradient("GAME OVER!", font, screen, 100, 270)
            draw_text_with_gradient("Вернитесь в меню", font, screen, 10, 300)
            draw_text_with_gradient("или начните игру", font, screen, 10, 330)
            draw_text_with_gradient("заново", font, screen, 150, 360)
            if pygame.mouse.get_pressed()[0]:
                # Перезапуск игры
                blocks.clear()
                score = 0
                level = 1
                FALL_SPEED = 5
                game_over = False

        pygame.display.flip()
        clock.tick(40)

    pygame.quit()
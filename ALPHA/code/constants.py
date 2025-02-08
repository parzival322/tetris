new_data_counter = 0
top_score_classic = 0
top_score_modern = 0
top_score_genius = 0

import pygame
import sys
import os
from psql import *


pygame.init()

pygame.display.set_caption("Tetris")

background_color = (30, 30, 30)
button_color = (100, 100, 255)
button_hover_color = (150, 150, 255)

# Шрифты
font = pygame.font.Font('./assets/font_main.ttf', 18)

screen_width = 500
screen_height = 650
screen = pygame.display.set_mode((500, 650), pygame.NOFRAME)
clock = pygame.time.Clock()

#cursor
bitmap = pygame.cursors.Cursor(*pygame.cursors.arrow)
cursors = [bitmap]
cursor_index = 0

# ПЕРЕМЕННЫЕ ДЛЯ ЛИДЕРБОРДЫ
leaders = get_data_from_table()

# Цвета для переливания
colors_gradient = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
color_index = 0
last_color_change_time = pygame.time.get_ticks()
COLOR_CHANGE_INTERVAL = 500


def draw_button(text, x, y, width, height, hovered):
    # Цвета для кнопки
    button_color = (255,211,155)  # Основной цвет
    hover_color = (205,170,125)    # Цвет при наведении
    shadow_color = (0, 0, 0, 100)  # Цвет тени
    text_color = (0,0,0)   # Цвет текста

    # Закругленные углы
    border_radius = 15

    # Тень кнопки
    shadow_offset = 5
    shadow_rect = pygame.Rect(x + shadow_offset, y + shadow_offset, width, height)
    pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=border_radius)

    # Основной прямоугольник кнопки
    button_rect = pygame.Rect(x, y, width, height)
    if hovered:
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=border_radius)
    else:
        pygame.draw.rect(screen, button_color, button_rect, border_radius=border_radius)

    # Текст кнопки
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_text_with_gradient(text, font, surface, x, y):
    global color_index, last_color_change_time
    current_time = pygame.time.get_ticks()
    if current_time - last_color_change_time >= COLOR_CHANGE_INTERVAL:
        color_index = (color_index + 1) % len(colors_gradient)
        last_color_change_time = current_time
    color = colors_gradient[color_index]
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main_menu(classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func, username, volume=0.5):
    global screen, draw_text_with_gradient, font

    nickname = username

    screen = pygame.display.set_mode((500, 650))
    
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

    pygame.mouse.set_cursor(cursors[cursor_index])

    pygame.mixer.init()
    pygame.mixer.music.load("./assets/music.mp3")  # Убедитесь, что файл music.mp3 находится в той же директории, что и ваш скрипт
    pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть в цикле
    music_on = True
    music_on_checker = True
    pygame.mixer.music.set_volume(volume)  # Устанавливаем начальную громкость


    while True:
        screen.fill(background_color)
        font1 = pygame.font.Font('./assets/font_main.ttf', 100)
        text_width, text_height = font1.size("TETRIS")
        draw_text_with_gradient("TETRIS", font1, screen, (screen_width - text_width) // 2, 75)

        nickname_text = font.render(f"{nickname}", True, (255, 255, 255))
        screen.blit(nickname_text, (400, 620))
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= mouse_pos[0] <= 350 and 200 <= mouse_pos[1] <= 250:
                    classic_tetris_func(leaders, nickname, music_on_checker, volume)
                if 150 <= mouse_pos[0] <= 350 and 300 <= mouse_pos[1] <= 350:
                    modern_tetris_func(leaders, nickname, music_on_checker, volume)
                if 150 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 450:
                    genius_mode_func(leaders, nickname, music_on_checker, volume)
                if 150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550:
                    leaderboard_menu_func(leaders, nickname, volume)
                    return
                # Кнопка "Музыка: Вкл/Выкл"
                if 25 <= mouse_pos[0] <= 100 and 350 <= mouse_pos[1] <= 400:
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.unpause()
                        music_on_checker = True
                    else:
                        pygame.mixer.music.pause()
                        music_on_checker = False
                # Увеличение громкости
                if 25 <= mouse_pos[0] <= 75 and 315 <= mouse_pos[1] <= 340:
                    volume = min(1.0, volume + 0.1)  # Увеличиваем громкость на 10%
                    pygame.mixer.music.set_volume(volume)
                # Уменьшение громкости
                if 25 <= mouse_pos[0] <= 75 and 410 <= mouse_pos[1] <= 430:
                    volume = max(0.0, volume - 0.1)  # Уменьшаем громкость на 10%
                    pygame.mixer.music.set_volume(volume)

        # Отрисовка кнопок
        draw_button(
            "Классический",
            150,
            200,
            200,
            50,
            150 <= mouse_pos[0] <= 350 and 200 <= mouse_pos[1] <= 250,
        )
        draw_button(
            "Современный",
            150,
            300,
            200,
            50,
            150 <= mouse_pos[0] <= 350 and 300 <= mouse_pos[1] <= 350,
        )
        draw_button(
            "Гениальный",
            150,
            400,
            200,
            50,
            150 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 450,
        )
        draw_button(
            "Лидеры",
            150,
            500,
            200,
            50,
            150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550,
        )
        draw_button(
            "Вкл" if music_on else "Выкл",
            25,
            350,
            50,
            50,
            50 <= mouse_pos[0] <= 100 and 350 <= mouse_pos[1] <= 400,
        )

        # Кнопки для регулировки громкости
        draw_button("+", 25, 315, 50, 25, 25 <= mouse_pos[0] <= 100 and 315 <= mouse_pos[1] <= 340)
        draw_button("-", 25, 410, 50, 25, 25 <= mouse_pos[0] <= 100 and 410 <= mouse_pos[1] <= 440)
        # Отображение текущей громкости
        volume_text = font.render(f"{int(round(volume * 100))}%", True, (255, 255, 255))
        screen.blit(volume_text, (25, 280))

        pygame.display.flip()

def go_back_to_main_menu(classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func, username, volume):
    main_menu(classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func, username, volume)
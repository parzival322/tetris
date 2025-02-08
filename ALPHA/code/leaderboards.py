import pygame
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

# Цвета для переливания
colors_gradient = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
COLOR_CHANGE_INTERVAL = 500
last_color_change_time = pygame.time.get_ticks()
color_index = 0

# Функция для отображения текста с переливанием
def draw_text_with_gradient(text, font, surface, x, y):
    global last_color_change_time, color_index
    current_time = pygame.time.get_ticks()
    if current_time - last_color_change_time >= COLOR_CHANGE_INTERVAL:
        color_index = (color_index + 1) % len(colors_gradient)
        last_color_change_time = current_time
    color = colors_gradient[color_index]
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def leaderboard_menu(leaders, username, volume):

    screen = pygame.display.set_mode((500, 650))

    try:
        insert_into_table(leaders)
    except Exception:
        pass

    while True:
        screen.fill(background_color)
        mouse_pos = pygame.mouse.get_pos()

        font1 = pygame.font.Font('./assets/font_main.ttf', 100)
        text_width, text_height = font1.size("ЛИДЕРЫ")
        draw_text_with_gradient("ЛИДЕРЫ", font1, screen, (screen_width - text_width) // 2, 65)

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
            "Выйти",
            150,
            500,
            200,
            50,
            150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550,
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 150 <= mouse_pos[0] <= 350 and 200 <= mouse_pos[1] <= 250:
                    classic_leaderboard(leaders, username, volume)
                if 150 <= mouse_pos[0] <= 350 and 300 <= mouse_pos[1] <= 350:
                    modern_leaderboard(leaders, username, volume)
                if 150 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 450:
                    genius_leaderboard(leaders, username, volume)
                if 150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550:
                    from constants import go_back_to_main_menu
                    from games import classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func
                    go_back_to_main_menu(classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func, username, volume)

def classic_leaderboard(leaders, username, volume):
    global screen, background_color

    classic_leaders = LeaderBoard('Классический', leaders, username, volume)
    classic_leaders.draw_leaderboard()

def modern_leaderboard(leaders, username, volume):
    global screen, background_color

    modern_leaders = LeaderBoard('Современный', leaders, username, volume)
    modern_leaders.draw_leaderboard()

def genius_leaderboard(leaders, username, volume):
    global screen, background_color

    genius_leaders = LeaderBoard('Гениальный', leaders, username, volume)
    genius_leaders.draw_leaderboard()

class LeaderBoard:
    def __init__(self, mode, leaderboard, username, volume):
        global background_color
        self.mode = mode
        self.leaderboard = leaderboard
        self.font = pygame.font.Font("./assets/font_main.ttf", 30)
        self.screen = pygame.display.set_mode((500, 650))
        self.clock = pygame.time.Clock()
        self.background = background_color
        self.username = username
        self.volume = volume

    def back_to_leaderboard_menu(self):
        leaderboard_menu(self.leaderboard, self.username, self.volume)

    def draw_leaderboard(self):
        while True:
            self.screen.fill(self.background)

            leaders_header = font.render("Лидеры:", True, (255, 255, 255))
            screen.blit(leaders_header, (200, 10))


            # Сортировка таблицы лидеров
            sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1][1], reverse=True)
            
            classic_leaders = []
            for (nickname, scores) in sorted(sorted_leaderboard, key=lambda x: x[1][0], reverse=True):
                if scores[0] > 0:
                    classic_leaders.append((nickname, scores[0]))

            modern_leaders = []
            for (nickname, scores) in sorted(sorted_leaderboard, key=lambda x: x[1][1], reverse=True):
                if scores[1] > 0:
                    modern_leaders.append((nickname, scores[1]))

            genius_leaders = []
            for (nickname, scores) in sorted(sorted_leaderboard, key=lambda x: x[1][2], reverse=True):
                if scores[2] > 0:
                    genius_leaders.append((nickname, scores[2]))

            classic_limit_counter = 0
            modern_limit_counter = 0
            genius_limit_counter = 0

            if self.mode == 'Классический':
                for i, (nickname, scores) in enumerate(sorted(classic_leaders, key=lambda score: classic_leaders[1], reverse=True)):
                    if scores > 0:
                        if classic_limit_counter <= 10:
                            leader = font.render(
                                f"{i+1}. {nickname} - {scores}",
                                True, 
                                (255, 255, 255))
                            screen.blit(leader, (150, 50 + i * 50))
                            classic_limit_counter += 1
            if self.mode == 'Современный':
                for i, (nickname, scores) in enumerate(sorted(modern_leaders, key=lambda score: modern_leaders[1], reverse=True)):
                    if scores > 0:
                        if modern_limit_counter <= 10:
                            leader = font.render(
                                f"{i+1}. {nickname} - {scores}",
                                True, 
                                (255, 255, 255))
                            screen.blit(leader, (150, 50 + i * 50))
                            modern_limit_counter += 1
            if self.mode == 'Гениальный':
                for i, (nickname, scores) in enumerate(sorted(genius_leaders, key=lambda score: genius_leaders[1], reverse=True)):
                    if scores > 0:
                        if genius_limit_counter <= 10:
                            leader = font.render(
                                f"{i+1}. {nickname} - {scores}",
                                True, 
                                (255, 255, 255))
                            screen.blit(leader, (150, 50 + i * 50))
                            genius_limit_counter += 1

            pygame.display.flip()
            self.clock.tick(60)

            while True:
                mouse_pos = pygame.mouse.get_pos()

                draw_button(
                    "Выйти",
                    150,
                    500,
                    200,
                    50,
                    150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550,
                )

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 150 <= mouse_pos[0] <= 350 and 500 <= mouse_pos[1] <= 550:
                            self.back_to_leaderboard_menu()
                            return
import pygame
import sys
import os
from psql import *
from games import classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func
from constants import main_menu
from loginwindow import login_window

def main(username):
    main_menu(classic_tetris_func, modern_tetris_func, genius_mode_func, leaderboard_menu_func, username)


if __name__ == "__main__":
    data = login_window()
    if data['status'] == True:
        main(data['username'])
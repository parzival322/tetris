from first import classic_tetris
from second import modern_tetris
from third import genius_mode
from leaderboards import leaderboard_menu

def classic_tetris_func(leaders, nickname, music_on_checker, volume):
    return classic_tetris(leaders, nickname, music_on_checker, volume)

def modern_tetris_func(leaders, nickname, music_on_checker, volume):
    return modern_tetris(leaders, nickname, music_on_checker, volume)

def genius_mode_func(leaders, nickname, music_on_checker, volume):
    return genius_mode(leaders, nickname, music_on_checker, volume)

def leaderboard_menu_func(leaders, nickname, volume):
    return leaderboard_menu(leaders, nickname, volume)

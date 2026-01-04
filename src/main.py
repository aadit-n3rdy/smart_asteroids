"""
Initiates pygame
Loads the main menu at the start of the game
Manages the 'state' of the game
Loads  different 'states'
"""
import pygame as pg
from src.core.game_states import GAME_STATES
import src.ui.main_menu as main_menu
import src.core.game as game
from src.utils.constants import window_height, window_width

pg.init()
screen_size = (window_width, window_height)
surface = pg.display.set_mode(screen_size)

game_state = GAME_STATES.MAIN_MENU

while game_state != GAME_STATES.QUIT:
    if game_state == GAME_STATES.MAIN_MENU:
        game_state = main_menu.main_menu(surface)
    elif game_state == GAME_STATES.IN_GAME:
        game_state = game.ingame(surface)

pg.quit()

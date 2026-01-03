"""
Displays the main menu
Allows user to play  or quit
"""
import pygame
import pygame_gui
import src.utils.constants as constants
from src.utils.constants import get_asset_path
import src.core.game_states as game_states

background_color = (100, 100, 100)

def main_menu(surface: pygame.surface.Surface):

    """
    Initiates a few required variables
    (GUI management, fonts, text)
    """
    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height), get_asset_path('themes/main_menu_theme.json'))
    clock = pygame.time.Clock()
    font = pygame.font.Font(get_asset_path("fonts/ARCADECLASSIC.TTF"), 98)
    title_img = font.render("Smart Asteroids", True,
                            (200, 200, 200, 200), background_color)
    title_rect = title_img.get_rect()
    title_rect.center = (constants.window_width*0.5,
                         constants.window_height*235/720)
    title_rect.size = (constants.window_width*700//1280,
                       constants.window_height*250//720)
    play_button_rect = pygame.Rect((constants.window_width*470//1280, constants.window_height*405//720),
                                   (constants.window_width*340//1280, constants.window_height*80//720))
    play_button = pygame_gui.elements.UIButton(
        relative_rect=play_button_rect, text="Play", manager=gui_manager)
    
    standard_button_rect = pygame.Rect((constants.window_width*470//1280, constants.window_height*467//720),
                                    (constants.window_width*340//1280, constants.window_height*80//720))
    standard_button = pygame_gui.elements.UIButton(
        relative_rect=standard_button_rect, text="Standard Mode", manager=gui_manager)

    quit_button_rect = pygame.Rect((constants.window_width*470//1280, constants.window_height*529//720),
                                   (constants.window_width*340//1280, constants.window_height*80/720))
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=quit_button_rect, text="Quit", manager=gui_manager)

    is_running = True
    while is_running:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        return (game_states.GAME_STATES.IN_GAME, False) # Standard Mode = False
                    elif event.ui_element == standard_button:
                        return (game_states.GAME_STATES.IN_GAME, True) # Standard Mode = True
                    elif event.ui_element == quit_button:
                        return (game_states.GAME_STATES.QUIT, False)
            gui_manager.process_events(event)

        gui_manager.update(dt)

        surface.fill(background_color)
        surface.blit(title_img, title_rect)
        gui_manager.draw_ui(surface)

        pygame.display.update()

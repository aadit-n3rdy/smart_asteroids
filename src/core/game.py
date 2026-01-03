"""
Game state, include the pause menu and the game over menu
"""


import pygame
import pygame_gui
import numpy
from src.core import constants
from src.core.constants import get_asset_path
from src.core.game_states import GAME_STATES
from src.entities import rocket
from src.entities import asteroid

background_color = (0, 0, 0)


def calc_quality(ast : asteroid.asteroid):
    return - ast.avg_dist_sqrt * ast.avg_dist_samples

def ingame(surface: pygame.surface.Surface):

    """
    Create the asteroids
    Initialise necessary variables
    """
    asteroid_count = 8
    clock = pygame.time.Clock()
    font_path = get_asset_path('fonts', 'ARCADECLASSIC.TTF')
    font = pygame.font.Font(font_path, 48)
    score = 0
    score_img = font.render(
        str(score), True, (200, 200, 200), background_color)
    score_rect = score_img.get_rect()
    score_rect.topright = (constants.window_width - 30, 30)
    asteroids_group = pygame.sprite.Group()
    for i in range(0, asteroid_count):
        tmp_start_vel = [0, 0]
        tmp_start_pos = [0, 0]
        if numpy.random.random() < 0.5:
            tmp_start_pos = [-constants.asteroid_radius, constants.window_height *
                             (0.1 + numpy.random.random()*0.8)]
            tmp_start_vel = [constants.asteroid_start_vel, 0]
        else:
            tmp_start_pos = [constants.window_width + constants.asteroid_radius,
                             constants.window_height * numpy.random.random()]
            tmp_start_vel = [-constants.asteroid_start_vel, 0]
        tmp = asteroid.asteroid(asteroid_count, numpy.array(tmp_start_pos),
                                constants.generalise_height(constants.asteroid_radius),
                                numpy.array(tmp_start_vel))
        asteroids_group.add(tmp)
    player = rocket.rocket()
    bullets = []
    parent = None
    parent_qual = 0
    last_best_check_tick = -1000

    is_running = True
    while is_running:

        """
        Calculate the time taken for the previous frame and cap FPS to 60
        """
        dt = clock.tick(60)/1000.0

        """
        Handle input and quit events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    ret = pause_menu(surface)
                    if ret != GAME_STATES.IN_GAME:
                        return ret

        """
        If the player is dead, display the game over menu
        """
        if player.status == rocket.ROCKET_STATUS.DEAD:
            return game_over_menu(surface, score)

        """
        Update positions and velocities of bullets, asteroids and player
        """
        asteroids_group.update(asteroids_group, player, dt, bullets)
        player.update(asteroids_group, dt, bullets)
        for i in range(0, len(bullets)):
            bullets[i].update(dt)

        """
        Remove destroyed asteroids,
        and create new ones if necessary
        """
        to_be_removed = []
        if parent is None:
            parent = asteroids_group.sprites()[0]
            parent_qual = calc_quality(parent)
        for a in asteroids_group:
            qual = calc_quality(a)
            if qual > parent_qual:
                parent = a
                parent_qual = qual
        for ast in asteroids_group:
            if ast.status == asteroid.ASTEROID_STATUS.DESTROYED:
                to_be_removed.append(ast)
                if ast.destroyed_by_player:
                    """
                    Increment the score and update the score display
                    if an asteroid has been destroyed by the player
                    """
                    score += 1
                    score_img = font.render(
                        str(score), True, (200, 200, 200), background_color)
                    score_rect = score_img.get_rect()
                    score_rect.topright = (constants.window_width-30, 30)
        for r in to_be_removed:
            asteroids_group.remove(r)
            tmp_start_vel = [0, 0]
            tmp_start_pos = [0, 0]
            if numpy.random.random() < 0.5:
                tmp_start_pos = [0 - constants.asteroid_radius, constants.window_height *
                                 (0.1 + numpy.random.random()*0.8)]
                tmp_start_vel = [constants.asteroid_start_vel, 0]
            else:
                tmp_start_pos = [constants.window_width + constants.asteroid_radius,
                                 constants.window_height * numpy.random.random()]
                tmp_start_vel = [-constants.asteroid_start_vel, 0]
            tmp = asteroid.asteroid(asteroid_count, numpy.array(tmp_start_pos),
                                    constants.generalise_height(constants.asteroid_radius),
                                    numpy.array(tmp_start_vel))
            tmp.evolve_from(parent)
            asteroids_group.add(tmp)
        to_be_removed = []

        """
        Clear the background and draw the player, asteroids
        and the bullets
        """
        surface.fill(background_color)
        for i in range(0, len(bullets)):
            pos = bullets[i].position
            if pos[0] < 0 or pos[0] > constants.window_width or pos[1] < 0 or\
               pos[1] > constants.window_height:
                to_be_removed.append(bullets[i])
            bullets[i].draw(surface)
        for i in to_be_removed:
            bullets.remove(i)
        asteroids_group.draw(surface)
        surface.blit(player.image, player.rect)
        surface.blit(score_img, score_rect)

        pygame.display.update()


def pause_menu(surface: pygame.surface.Surface):

    """
    Displays the pause menu
    """
    menu_rect = pygame.rect.Rect((constants.window_width//4, constants.window_width//4),
                                 (constants.window_width//2, constants.window_height//2))
    menu_rect.center = (constants.window_width//2, constants.window_height//2)
    paused_background = (50, 50, 50)
    paused_foreground = (200, 200, 200)

    theme_path = get_asset_path('themes', 'pause_menu_theme.json')
    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height), theme_path)
    clock = pygame.time.Clock()
    font_path = get_asset_path('fonts', 'ARCADECLASSIC.TTF')
    font = pygame.font.Font(font_path,
                            constants.generalise_height(75))
    pause_img = font.render("game paused", True,
                            paused_foreground, paused_background)
    pause_rect = pause_img.get_rect()
    pause_rect.center = (constants.generalise_width(640),
                         constants.generalise_height(292))

    resume_button_rect = pygame.Rect((constants.generalise_width(549),
                                      constants.generalise_height(350)),
                                     (constants.generalise_width(164),
                                      constants.generalise_height(41)))
    quit_button_rect = pygame.Rect((constants.generalise_width(549),
                                    constants.generalise_height(409)),
                                   (constants.generalise_width(164),
                                    constants.generalise_height(41)))
    menu_button_rect = pygame.Rect((constants.generalise_width(549),
                                    constants.generalise_height(468)),
                                   (constants.generalise_width(164),
                                    constants.generalise_height(41)))

    resume_button = pygame_gui.elements.UIButton(
        relative_rect=resume_button_rect, text="Resume", manager=gui_manager)
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=quit_button_rect, text="Quit", manager=gui_manager)
    menu_button = pygame_gui.elements.UIButton(
        relative_rect=menu_button_rect, text="Exit to menu", manager=gui_manager)

    is_paused = True
    while is_paused:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == quit_button:
                        return GAME_STATES.QUIT
                    if event.ui_element == resume_button:
                        return GAME_STATES.IN_GAME
                    if event.ui_element == menu_button:
                        return GAME_STATES.MAIN_MENU

            gui_manager.process_events(event)

        gui_manager.update(dt)

        surface.fill(paused_background, menu_rect)
        surface.blit(pause_img, pause_rect)
        gui_manager.draw_ui(surface)

        pygame.display.update(menu_rect)


def game_over_menu(surface: pygame.surface.Surface, score: int):

    """
    Displays the game over menu
    """

    menu_rect = pygame.rect.Rect((constants.window_width//4, constants.window_width//4),
                                 (constants.window_width//2, constants.window_height//2))
    menu_rect.center = (constants.window_width//2, constants.window_height//2)
    over_background = (50, 50, 50)
    over_foreground = (200, 200, 200)

    theme_path = get_asset_path('themes', 'game_over_theme.json')
    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height), theme_path)
    clock = pygame.time.Clock()
    font_path = get_asset_path('fonts', 'ARCADECLASSIC.TTF')
    font = pygame.font.Font(font_path,
                            constants.generalise_height(75))
    over_img = font.render("game over", True,
                           over_foreground, over_background)
    over_rect = over_img.get_rect()
    over_rect.center = (constants.generalise_width(640),
                        constants.generalise_height(292))

    score_font = pygame.font.Font(
        font_path, constants.generalise_height(48))
    string = "Score is " + str(score)
    score_img = score_font.render(string, True, over_foreground, over_background)
    score_rect = score_img.get_rect()
    score_rect.center = (constants.generalise_width(
        549+82), constants.generalise_height(370))

    restart_button_rect = pygame.Rect((constants.generalise_width(549), constants.generalise_height(
        409)), (constants.generalise_width(164), constants.generalise_height(41)))
    quit_button_rect = pygame.Rect((constants.generalise_width(549), constants.generalise_height(
        468)), (constants.generalise_width(164), constants.generalise_height(41)))

    restart_button = pygame_gui.elements.UIButton(
        relative_rect=restart_button_rect, text="restart", manager=gui_manager)
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=quit_button_rect, text="Exit to menu", manager=gui_manager)

    is_paused = True
    while is_paused:
        dt = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == quit_button:
                        return GAME_STATES.MAIN_MENU
                    if event.ui_element == restart_button:
                        return GAME_STATES.IN_GAME
            gui_manager.process_events(event)
        gui_manager.update(dt)

        surface.fill(over_background, menu_rect)
        surface.blit(over_img, over_rect)
        surface.blit(score_img, score_rect)
        gui_manager.draw_ui(surface)

        pygame.display.update(menu_rect)

import pygame
import pygame_gui

import src.utils.constants as constants
from src.utils.constants import get_asset_path
from src.core.game_states import GAME_STATES

INCH_PX = 96


def user_guide(surface: pygame.Surface):
    clock = pygame.time.Clock()

    # Use same theme as main menu (restores button font)
    gui_manager = pygame_gui.UIManager(
        (constants.window_width, constants.window_height),
        get_asset_path("themes/main_menu_theme.json")
    )

    # ---------------- Back Button ----------------
    back_button_rect = pygame.Rect(
        (constants.window_width * 470 // 1280,
         constants.window_height * 600 // 720),
        (constants.window_width * 340 // 1280,
         constants.window_height * 80 // 720)
    )

    back_button = pygame_gui.elements.UIButton(
        relative_rect=back_button_rect,
        text="Back",
        manager=gui_manager
    )

    # ---------------- Scroll State ----------------
    scroll_offset = 0
    SCROLL_SPEED = 30

    # ---------------- Text Viewport Geometry ----------------
    container_width = int(constants.window_width * 0.6)
    container_x = (constants.window_width - container_width) // 2

    text_top = INCH_PX
    text_bottom = back_button_rect.top - INCH_PX
    viewport_height = text_bottom - text_top

    viewport_rect = pygame.Rect(
        container_x,
        text_top,
        container_width,
        viewport_height
    )

    # ---------------- Fonts ----------------
    font_title = pygame.font.Font(get_asset_path("fonts/ARCADECLASSIC.TTF"), 40)
    font_h2 = pygame.font.Font(get_asset_path("fonts/ARCADECLASSIC.TTF"), 30)
    font_h3 = pygame.font.Font(get_asset_path("fonts/ARCADECLASSIC.TTF"), 26)
    font_body = pygame.font.Font(get_asset_path("fonts/ARCADECLASSIC.TTF"), 22)

    # ---------------- Load Markdown ----------------
    with open("docs/USER_GUIDE.md", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # ---------------- Parse Markdown ----------------
    rendered_items = []
    y = 0
    line_spacing = 8

    for line in lines:
        line = line.rstrip()

        # Horizontal rule
        if line.strip() == "---":
            rendered_items.append(("HR", None))
            y += 20
            continue

        # Title
        if line.startswith("# "):
            text = line[2:]
            surf = font_title.render(text, True, (240, 240, 240))
            rendered_items.append(("TEXT", surf, 0))
            y += surf.get_height() + 20
            continue

        # Section header
        if line.startswith("## "):
            text = line[3:]
            surf = font_h2.render(text, True, (235, 235, 235))
            rendered_items.append(("TEXT", surf, 0))
            y += surf.get_height() + 16
            continue

        # Subsection header
        if line.startswith("### "):
            text = line[4:]
            surf = font_h3.render(text, True, (230, 230, 230))
            rendered_items.append(("TEXT", surf, 0))
            y += surf.get_height() + 14
            continue

        # Bullet
        if line.startswith("- "):
            text = "• " + line[2:].replace("**", "")
            surf = font_body.render(text, True, (220, 220, 220))
            rendered_items.append(("TEXT", surf, 24))  # indent
            y += surf.get_height() + line_spacing
            continue

        # Empty line
        if line == "":
            y += 12
            continue

        # Body text
        text = line.replace("**", "")
        surf = font_body.render(text, True, (220, 220, 220))
        rendered_items.append(("TEXT", surf, 0))
        y += surf.get_height() + line_spacing

    # ---------------- Build Text Surface ----------------
    text_surface = pygame.Surface(
        (container_width, max(y, viewport_height)),
        pygame.SRCALPHA
    )

    y = 0
    for item in rendered_items:
        if item[0] == "HR":
            pygame.draw.line(
                text_surface,
                (160, 160, 160),
                (0, y),
                (container_width, y),
                2
            )
            y += 20
        else:
            _, surf, indent = item
            text_surface.blit(surf, (indent, y))
            y += surf.get_height() + line_spacing

    # ---------------- Main Loop ----------------
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_STATES.QUIT

            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += -event.y * SCROLL_SPEED

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        return GAME_STATES.MAIN_MENU

            gui_manager.process_events(event)

        # Clamp scrolling
        max_scroll = max(0, text_surface.get_height() - viewport_height)
        scroll_offset = max(0, min(scroll_offset, max_scroll))

        # ---------------- Drawing ----------------
        surface.fill((60, 60, 60))

        pygame.draw.rect(surface, (80, 80, 80), viewport_rect)

        surface.set_clip(viewport_rect)
        surface.blit(
            text_surface,
            (container_x, text_top - scroll_offset)
        )
        surface.set_clip(None)

        gui_manager.update(dt)
        gui_manager.draw_ui(surface)
        pygame.display.update()

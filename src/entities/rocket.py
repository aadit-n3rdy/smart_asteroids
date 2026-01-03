"""
Defines the rocket class
"""

import numpy as np
import pygame
import enum
from src.core.constants import window_width
from src.core.constants import window_height
from src.core.constants import generalise_height
from src.core.constants import rocket_accel_coeff
from src.core.constants import rocket_velocity_coeff
from src.core.constants import get_asset_path
from src.entities import bullet


class ROCKET_STATUS(enum.Enum):
    ALIVE = 0
    DEAD = 1


class rocket(pygame.sprite.Sprite):
    """
    rocket class: derives from pygame sprite
    """
    position: np.array
    velocity: np.array
    angle: float
    status: ROCKET_STATUS
    image: pygame.surface.Surface
    rect: pygame.rect.Rect
    unrotated_image: pygame.surface.Surface
    last_shot_tick: float

    def __init__(self):
        super().__init__()
        self.position = np.array((window_width/2, window_height/2))
        self.velocity = np.array([0.0, 0.0])
        self.angle = 0.0
        self.status = ROCKET_STATUS.ALIVE
        asset_path = get_asset_path('images', 'rocket2.png')
        self.unrotated_image = pygame.transform.smoothscale(pygame.image.load(
            asset_path).convert_alpha(),
            (generalise_height(20), generalise_height(20)))
        self.last_shot_tick = -1000

    def update(self, asteroids: pygame.sprite.Group, dt: float, bullets: list):
        if self.status == ROCKET_STATUS.ALIVE:
            """
            Calculates the angle made by the mouse pointer with the horizontal
            """
            (mousex, mousey) = pygame.mouse.get_pos()
            mousex -= self.position[0]
            mousey -= self.position[1]
            magnitude = (mousex**2 + mousey**2)**0.5
            angle_sin = mousey/magnitude
            angle_cos = mousex/magnitude
            self.angle = np.arctan2(-mousey, mousex)

            """
            Accelerate towards mouse pointer if LMB is pressed
            """
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.velocity[0] += rocket_accel_coeff * dt * angle_cos
                self.velocity[1] += rocket_accel_coeff * dt * angle_sin

            """
            Fire if last shot was fired > 0.2 seconds ago and RMB is pressed
            """
            if pygame.mouse.get_pressed()[2] and \
               (pygame.time.get_ticks() - self.last_shot_tick)/1000 >= 0.1:
                bullets.append(bullet.bullet(self.position.copy(), self.angle))
                self.last_shot_tick = pygame.time.get_ticks()

            """
            Update position, rotate image, check for collisions
            """
            self.position[0] += rocket_velocity_coeff * dt * self.velocity[0]
            self.position[1] += rocket_velocity_coeff * dt * self.velocity[1]
            self.image = pygame.transform.rotate(
                self.unrotated_image, np.degrees(self.angle)-90)
            self.rect = self.image.get_rect()
            self.rect.center = (self.position[0], self.position[1])
            for asteroid in asteroids:
                if pygame.sprite.collide_mask(self, asteroid):
                    self.status = ROCKET_STATUS.DEAD
            if self.position[0] < 0 or self.position[0] > window_width or \
               self.position[1] < 0 or self.position[1] > window_height:
                self.status = ROCKET_STATUS.DEAD

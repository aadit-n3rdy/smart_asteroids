import numpy as np
import pygame
import constants


class bullet():
    position: np.array
    velocity: np.array

    def __init__(self, position, angle):
        self.position = position
        self.velocity = np.array((np.cos(angle), -np.sin(angle)))
        self.velocity = self.velocity * constants.bullet_velocity

    def update(self, dt):
        ds = self.velocity * dt
        self.position = self.position + ds

    def draw(self, surface):
        pygame.draw.circle(surface, (200, 200, 200),
                           (self.position[0], self.position[1]), 3)

import numpy as np
import enum
import pygame
from src.ai.neural_network import neural_network
from src.entities import rocket
from src.core.constants import *
from src.core.constants import get_asset_path
from src.entities import bullet


class ASTEROID_STATUS(enum.Enum):
    ALIVE = 0
    DESTROYED = 1


class asteroid(pygame.sprite.Sprite):
    destroyed_by_player: bool
    network: neural_network = None
    position: np.array = None
    velocity: np.array = None
    status: ASTEROID_STATUS = ASTEROID_STATUS.ALIVE
    network_inp_count: int
    image: pygame.surface.Surface
    radius: float
    rect: pygame.rect.Rect
    avg_dist_sqrt: float
    avg_dist_samples: float
    last_avg_dist_sample_tick: float
    least_dist_sq: float

    def __init__(self, asteroid_count: int, start_position: np.array,
                 radius: float, start_velocity: np.array):

        """
        Initiate all asteroids with a usual parameters, generate a random
        spawn location, and rotate the asteroid by a random angle for each asteroid to be slightly different
        """
        super().__init__()
        self.destroyed_by_player = False
        self.network_inp_count = 2
        self.network = neural_network([self.network_inp_count, 2])
        self.position = start_position.flat.copy()
        self.velocity = np.array(start_velocity)
        self.status = ASTEROID_STATUS.ALIVE
        asset_path = get_asset_path('images', 'asteroid.png')
        self.image = pygame.transform.rotate(pygame.transform.smoothscale(
            pygame.image.load(asset_path).convert_alpha(),
            (2*int(generalise_height(radius)),
             2*int(generalise_height(radius)))), np.random.random()*360)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.radius = radius
        self.least_dist_sq = 0
        self.last_avg_dist_sample_tick = pygame.time.get_ticks()
        self.avg_dist_samples = 0
        self.avg_dist_sqrt = window_width**0.5

    def evolve_from(self, parent):
        self.network.from_parent(parent.network)

    def die(self):
        self.status = ASTEROID_STATUS.DESTROYED

    def update(self, asteroids: pygame.sprite.Group, player: rocket.rocket,
               dt: float, bullets: list):
        if self.status == ASTEROID_STATUS.ALIVE:
            """
            Calculates acceleration
            """
            inp = [None] * self.network_inp_count
            # inp[0] = self.velocity[0]
            # inp[1] = self.velocity[1]
            inp[0] = player.position[0] - self.position[0]
            inp[1] = player.position[1] - self.position[1]
            out = self.network.calculate(np.array(inp))

            """
            Updates the velocity and position
            """
            dx = player.position[0] - self.position[0]
            dy = player.position[1] - self.position[1]
            dist_sq = dx**2 + dy**2
            self.velocity[0] += out[0] + 0.001* dx * asteroid_accel_coeff * dt
            self.velocity[1] += out[1] + 0.001* dy * asteroid_accel_coeff * dt
            self.position[0] += self.velocity[0] * asteroid_vel_coeff * dt
            self.position[1] += self.velocity[1] * asteroid_vel_coeff * dt
            self.rect.center = (int(self.position[0]), int(self.position[1]))
            """
            Calculates the average square root of 
            the distance between asteroid and the player
            """
            if dist_sq < self.least_dist_sq or self.least_dist_sq < 0:
                self.least_dist_sq = dist_sq

            """
            Checks if asteroid has collided with another
            asteroid or bullet
            """
            asteroids.remove(self)
            for asteroid in asteroids:
                dx = asteroid.position[0] - self.position[0]
                dy = asteroid.position[1] - self.position[1]
                if dx**2 + dy**2 <= 4*(asteroid.radius+self.radius)**2:
                    self.die()
                    asteroid.die()
                    asteroids.add(self)
                    return
            asteroids.add(self)
            for bult in bullets:
                if self.rect.collidepoint(bult.position[0], bult.position[1]):
                    bullets.remove(bult)
                    self.destroyed_by_player = True
                    self.die()
                    return
            if (pygame.time.get_ticks() - self.last_avg_dist_sample_tick) /\
               1000 >= 0.01:
                dx = self.position[0] - target_position[0]
                dy = self.position[1] - target_position[1]
                if self.avg_dist_sqrt < 0:
                    self.avg_dist_sqrt
                total = self.avg_dist_sqrt * \
                    self.avg_dist_samples + (dx**2 + dy**2)**0.5
                self.avg_dist_samples += 1
                self.avg_dist_sqrt = total/self.avg_dist_samples
                self.last_avg_dist_sample_tick = pygame.time.get_ticks()
            if self.position[0] < 0-2*self.radius or\
               self.position[0] > window_width+2*self.radius or\
               self.position[1] < 0-2*self.radius or\
               self.position[1] > window_height+2*self.radius:
                self.die()
                return

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.image.get_rect(
            center=(int(self.position[0]), int(self.position[1]))))

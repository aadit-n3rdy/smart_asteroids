import random
import numpy as np
from src.evolution.base import BaseEvolution


class CrossoverEvolution(BaseEvolution):
    def evolve(self, child_network, parents):
        if len(parents) < 2:
            if len(parents) == 1:
                # take the first parent
                child_network.from_parent(parents[0].network)
            return

        # taking the first 2 of the parents for testing
        parent_a = parents[0].network
        parent_b = parents[1].network

        child_network.crossover_from_parents(parents[0].network, parents[1].network)

    def calculate_fitness(self, asteroid):
        return -asteroid.avg_dist_sqrt * asteroid.avg_dist_samples

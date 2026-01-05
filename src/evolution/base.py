import abc
import numpy as np

class BaseEvolution(abc.ABC):
    @abc.abstractmethod
    def evolve(self, child_network, parents):
        pass

    @abc.abstractmethod
    def calculate_fitness(self, asteroid):
        pass

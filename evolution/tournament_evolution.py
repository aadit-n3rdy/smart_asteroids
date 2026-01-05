import random
from evolution.base import BaseEvolution

class TournamentSelectionEvolution(BaseEvolution):
    def evolve(self, child_network, parents):
        if not parents:
            return

# intial size will be 3
        tournament_size = 3
        competitors = random.sample(parents, min(len(parents), tournament_size))
        competitors.sort(key=lambda x: self.calculate_fitness(x), reverse=True)
        
        best_parent = competitors[0].network
        child_network.learning_rate = best_parent.learning_rate
        
        for i in range(len(child_network.weights)):
            child_network.weights[i] = best_parent.weights[i].copy()
            for j in range(len(child_network.weights[i].flat)):
                mutation = child_network.learning_rate * random.randrange(-100000, 100000) / 100000.0
                child_network.weights[i].flat[j] += mutation

    def calculate_fitness(self, asteroid):
        return - asteroid.avg_dist_sqrt * asteroid.avg_dist_samples

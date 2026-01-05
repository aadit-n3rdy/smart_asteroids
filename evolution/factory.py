from evolution.crossover_evolution import CrossoverEvolution
from evolution.tournament_evolution import TournamentSelectionEvolution

def get_evolution_strategy(name):
    strategies = {
        "crossover": CrossoverEvolution,
        "tournament": TournamentSelectionEvolution
    }
    return strategies.get(name, CrossoverEvolution)()

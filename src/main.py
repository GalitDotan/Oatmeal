from src.init_simulation import init_simulated_annealing, run_simulated_annealing_with_prints


def main():
    simulated_annealing = init_simulated_annealing('french_deletion')
    run_simulated_annealing_with_prints(simulated_annealing)

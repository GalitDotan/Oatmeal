from src.init_simulation import init_simulated_annealing, run_simulated_annealing_with_prints

SIMULATION_NAME = 'bb_demote_only'


def main():
    simulated_annealing = init_simulated_annealing(SIMULATION_NAME)
    run_simulated_annealing_with_prints(simulated_annealing)


if __name__ == '__main__':
    main()

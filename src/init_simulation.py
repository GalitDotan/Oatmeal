import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

SIMULATIONS_DIR = 'simulations'


def init_simulated_annealing(simulation_name: str):
    """
    Initialize the simulated annealing process for a given simulation.

    Args:
        simulation_name (str): The name of the simulation directory containing the configuration files.

    Returns:
        SimulatedAnnealing: The initialized simulated annealing instance.
    """
    config_dir = os.path.join(SIMULATIONS_DIR, simulation_name)

    OtmlConfiguration.load(config_dir)

    feature_table = FeatureTable.load(settings.features_file)
    corpus = Corpus.load(settings.corpus_file)
    constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
    lexicon = Lexicon(corpus.get_words(), feature_table)

    initial_hypothesis = TraversableGrammarHypothesis(
        grammar=Grammar(
            feature_table,
            constraint_set, lexicon,
            grammar_name=simulation_name
        ),
        data=corpus.get_words()
    )
    return SimulatedAnnealing(initial_hypothesis)


def run_simulated_annealing_with_prints(simulated_annealing: SimulatedAnnealing) -> Grammar:
    """
    Run the simulated annealing process with intermediate prints for debugging.

    Args:
        simulated_annealing (SimulatedAnnealing): The initialized simulated annealing instance.

    Returns:
        Grammar: The final optimized grammar after the process.
    """
    print("Starting optimization")
    initial_grammar = simulated_annealing.current_hypothesis.grammar
    print(f'# Initial Lexicon: {initial_grammar.lexicon}')
    print(f'# Initial Feature table: {initial_grammar.feature_table}')
    print(f'# Initial Constraints Set: {initial_grammar.constraint_set}')

    step, hypothesis = simulated_annealing.run()
    final_grammar = simulated_annealing.current_hypothesis.grammar

    print(f'Ran {step} steps.')

    print(f'Initial hypothesis: {simulated_annealing.initial_hypothesis}')
    print(f'Final hypothesis: {simulated_annealing.current_hypothesis}')

    print(f'# Lexicon: {final_grammar.lexicon}')
    print(f'# Feature table: {final_grammar.feature_table}')
    print(f'# Constraints Set: {final_grammar.constraint_set}')
    return final_grammar


def init_simulated_annealing_categories(simulation_name: str):
    """
    Initialize simulated annealing processes for multiple lexical categories.

    Args:
        simulation_name (str): The name of the simulation directory containing the configuration files.

    Returns:
        tuple: A dictionary of simulated annealing instances for each category, and the corresponding corpora.
    """
    config_dir = os.path.join(SIMULATIONS_DIR, simulation_name)

    OtmlConfiguration.load(config_dir)

    feature_table = FeatureTable.load(settings.features_file)
    constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
    corpus_per_category = Corpus.load_corpus_per_category(settings.corpus_file)
    lexicon_per_category = {cat: Lexicon(corpus.get_words(), feature_table) for cat, corpus in
                            corpus_per_category.items()}
    lexical_categories = lexicon_per_category.keys()

    initial_hypothesis_per_category = {
        cat: TraversableGrammarHypothesis(
            grammar=Grammar(
                feature_table,
                constraint_set,
                lexicon_per_category[cat],
                grammar_name=f'{simulation_name}_{cat}',
            ),
            data=corpus_per_category[cat].get_words()
        ) for cat in lexical_categories}

    simulated_annealing_per_category = {cat: SimulatedAnnealing(initial_hypothesis) for cat, initial_hypothesis in
                                        initial_hypothesis_per_category.items()}
    return simulated_annealing_per_category, corpus_per_category


def run_simulated_annealing_with_prints_categories(
        simulated_annealing_per_category: dict[str, SimulatedAnnealing],
        corpus_per_category: dict[str, Corpus]) -> dict[str, Grammar]:
    """
    Run simulated annealing processes for each lexical category with intermediate prints.

    Args:
        simulated_annealing_per_category (dict): A dictionary of simulated annealing instances for each category.
        corpus_per_category (dict): A dictionary of corpora for each category.

    Returns:
        dict: A dictionary of final grammars for each category.
    """
    final_grammars = dict()

    for cat, simulated_annealing in simulated_annealing_per_category.items():
        if len(corpus_per_category[cat]) == 0:  # no words in this category
            continue
        print(f'Current lexical category: {cat}')
        final_grammars[cat] = run_simulated_annealing_with_prints(simulated_annealing)
    return final_grammars

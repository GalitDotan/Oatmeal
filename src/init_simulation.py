import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

SIMULATIONS_DIR = '..\\simulations'


def init_simulated_annealing(simulation_name: str):
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

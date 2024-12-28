import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

SIMULATION_NAME = 'SMH'
CONFIG_DIR = os.path.join('simulations', SIMULATION_NAME)

OtmlConfiguration.load(CONFIG_DIR)

feature_table = FeatureTable.load(settings.features_file)
constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
corpus_per_category = Corpus.load_corpus_per_category(settings.corpus_file)
lexicon_per_category = {cat: Lexicon(corpus.get_words(), feature_table) for cat, corpus in corpus_per_category.items()}
lexical_categories = lexicon_per_category.keys()

initial_hypothesis_per_category = {
    cat: TraversableGrammarHypothesis(
        grammar=Grammar(
            feature_table,
            constraint_set,
            lexicon_per_category[cat],
            grammar_name=f'{SIMULATION_NAME}_{cat}',
        ),
        data=corpus_per_category[cat].get_words()
    ) for cat in lexical_categories}

simulated_annealing_per_category = {cat: SimulatedAnnealing(initial_hypothesis) for cat, initial_hypothesis in
                                    initial_hypothesis_per_category.items()}

for cat, simulated_annealing in simulated_annealing_per_category.items():
    if len(corpus_per_category[cat]) == 0:  # no words in this category
        continue
    print(f'Starting optimization for {cat}')

    step, hypothesis = simulated_annealing.run()
    final_grammar = simulated_annealing.current_hypothesis.grammar

    print(f'Ran {step} steps.')

    print(f'Initial hypothesis: {simulated_annealing.initial_hypothesis}')
    print(f'Final hypothesis: {simulated_annealing.current_hypothesis}')

    print(f'# Lexicon: {final_grammar.lexicon}')
    print(f'# Feature table: {final_grammar.feature_table}')
    print(f'# Constraints Set: {final_grammar.constraint_set}')

    print(f'Finished optimization for {cat}')

print("Done")

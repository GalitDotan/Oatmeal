import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon, Word
from src.init_simulation import run_simulated_annealing_with_prints
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

SIMULATION_NAME = 'bb_demote_only'
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
    final_grammar = run_simulated_annealing_with_prints(simulated_annealing)

    """
    noH = Word(word_string="no'H", feature_table=final_grammar.feature_table)
    moreH = Word(word_string="more'H", feature_table=final_grammar.feature_table)
    hivliH = Word(word_string="hivli'H", feature_table=final_grammar.feature_table)
    niHbal = Word(word_string="niHba'l", feature_table=final_grammar.feature_table)
    print(f'{final_grammar.generate(noH)}, {final_grammar.generate(moreH)}, '
          f'{final_grammar.generate(hivliH)}, {final_grammar.generate(niHbal)}')
    """
    bb = Word(word_string="bb", feature_table=final_grammar.feature_table)
    abb = Word(word_string="abb", feature_table=final_grammar.feature_table)
    print(f'{final_grammar.generate(bb)}, {final_grammar.generate(abb)}')

    print(f'Finished optimization for {cat}')

print("Done")

import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

CONFIG_DIR = os.path.join('simulations', 'abnese')

OtmlConfiguration.load(CONFIG_DIR)

feature_table = FeatureTable.load(settings.features_file)
corpus = Corpus.load(settings.corpus_file)
constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
lexicon = Lexicon(corpus.get_words(), feature_table)

initial_hypothesis = TraversableGrammarHypothesis(grammar=Grammar(feature_table, constraint_set, lexicon),
                                                  data=corpus.get_words())
simulated_annealing = SimulatedAnnealing(initial_hypothesis)

print("Starting optimization")
step, hypothesis = simulated_annealing.run()

print(f'Ran {step} steps.')

print(f'Initial hypothesis: {simulated_annealing.initial_hypothesis}')
print(f'Final hypothesis: {simulated_annealing.current_hypothesis}')

print("Done")

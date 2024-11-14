import os

from src.grammar.constraint_set import ConstraintSet
from src.grammar.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.otml_configuration import OtmlConfiguration, settings
from src.simulated_annealing import SimulatedAnnealing

SIMULATION_NAME = 'french_deletion'

ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
CONFIG_DIR = os.path.join(ROOT_DIR, 'tests', 'fixtures', SIMULATION_NAME)

OtmlConfiguration.load(CONFIG_DIR)

feature_table = FeatureTable.load(settings.features_file)
corpus = Corpus.load(settings.corpus_file)
constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
lexicon = Lexicon(corpus.get_words(), feature_table)
grammar = Grammar(feature_table, constraint_set, lexicon)
data = corpus.get_words()
traversable_hypothesis = TraversableGrammarHypothesis(grammar, data)
simulated_annealing = SimulatedAnnealing(traversable_hypothesis)
step, hypothesis = simulated_annealing.run()
print(f'Ran {step} steps. Final hypothesis: {hypothesis}')

print("🥳️")

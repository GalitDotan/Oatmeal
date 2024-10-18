import os
from source.otml_configuration import OtmlConfiguration

CURRENT_PATH = os.path.split(os.path.abspath(__file__))[0]
FIXTURES_PATH = os.path.join(CURRENT_PATH, "tests/fixtures")

FEATURES_DIR = "feature_table"
CORPUS_DIR = "corpora"
CONSTRAINTS_DIR = "constraint_sets"
CONFIGS_DIR = "configuration"

SIMULATION_NAME = "french_deletion"

feature_table_file_path = f"{FIXTURES_PATH}/{FEATURES_DIR}/{SIMULATION_NAME}_feature_table.json"
corpus_file_path = f"{FIXTURES_PATH}/{CORPUS_DIR}/{SIMULATION_NAME}_corpus.txt"
constraint_set_file_path = f"{FIXTURES_PATH}/{CONSTRAINTS_DIR}/{SIMULATION_NAME}_constraint_set.json"

configuration_file_path = f"{FIXTURES_PATH}/{CONFIGS_DIR}/otml_configuration.json"

OtmlConfiguration.from_json(configuration_file_path)

from grammar.lexicon import Lexicon
from grammar.feature_table import FeatureTable
from grammar.constraint_set import ConstraintSet
from grammar.grammar import Grammar
from traversable_grammar_hypothesis import TraversableGrammarHypothesis
from corpus import Corpus
from simulated_annealing import SimulatedAnnealing

feature_table = FeatureTable.load(feature_table_file_path)
corpus = Corpus.load(corpus_file_path)
constraint_set = ConstraintSet.load(constraint_set_file_path, feature_table)
lexicon = Lexicon(corpus.get_words(), feature_table)
grammar = Grammar(feature_table, constraint_set, lexicon)
data = corpus.get_words()
traversable_hypothesis = TraversableGrammarHypothesis(grammar, data)
simulated_annealing = SimulatedAnnealing(traversable_hypothesis)
simulated_annealing.run()

print("🥳️")
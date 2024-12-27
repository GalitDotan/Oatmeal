import platform
import sys
import unittest

simulation_number = 1

from tests.test_logic.otml_configuration_for_testing import configurations
from src.grammar.lexicon import Lexicon
from src.grammar.feature_table import FeatureTable
from src.grammar.constraint_set import ConstraintSet
from src.grammar.grammar import Grammar
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.models.corpus import Corpus
from src.simulated_annealing import SimulatedAnnealing
from tests.test_logic.persistence_tools import get_constraint_set_fixture, get_feature_table_fixture, get_corpus_fixture
from tests import SimulationTestCase


class TestOtmlWithDLengthening(SimulationTestCase):
    def setUp(self):
        configurations["CONSTRAINT_SET_MUTATION_WEIGHTS"] = {
            "insert_constraint": 1,
            "remove_constraint": 1,
            "demote_constraint": 1,
            "insert_feature_bundle_phonotactic_constraint": 1,
            "remove_feature_bundle_phonotactic_constraint": 1,
            "augment_feature_bundle": 0}

        configurations["CONSTRAINT_INSERTION_WEIGHTS"] = {
            "Dep": 1,
            "Max": 1,
            "Ident": 0,
            "Phonotactic": 1}

        configurations["LEXICON_MUTATION_WEIGHTS"] = {
            "insert_segment": 1,
            "delete_segment": 1,
            "change_segment": 0}

        configurations["RANDOM_SEED"] = True
        # configurations["SEED"] = 84
        configurations["INITIAL_TEMPERATURE"] = 100
        configurations["COOLING_PARAMETER"] = 0.999985
        configurations["INITIAL_NUMBER_OF_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = 1
        configurations["MIN_FEATURE_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = 1
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 100
        configurations["RESTRICTION_ON_ALPHABET"] = True
        configurations["MAX_FEATURE_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = sys.maxsize
        configurations["MAX_NUMBER_OF_CONSTRAINTS_IN_CONSTRAINT_SET"] = sys.maxsize

        configurations["DEBUG_LOGGING_INTERVAL"] = 50
        configurations["LOG_FILE_NAME"] = "{}_d_lengthening_INF_INF_{}.txt".format(platform.node(), simulation_number)
        self._set_up_logging()
        configurations["CORPUS_DUPLICATION_FACTOR"] = 1
        self.feature_table = FeatureTable.load(get_feature_table_fixture("d_lengthening_feature_table.json"))
        corpus = Corpus.load(get_corpus_fixture("d_lengthening_corpus.txt"))
        self.constraint_set = ConstraintSet.load(get_constraint_set_fixture("faith_constraint_set.json"),
                                                 self.feature_table)
        self.lexicon = Lexicon(corpus.get_words(), self.feature_table)
        self.grammar = Grammar(self.feature_table, self.constraint_set, self.lexicon)
        self.data = corpus.get_words()
        self.traversable_hypothesis = TraversableGrammarHypothesis(self.grammar, self.data)

        def desired_lexicon_indicator_function(words):
            number_of_long_vowels = sum([word.count(":") for word in words])
            return "number of long vowels: {}".format(number_of_long_vowels)

        def convert_corpus_word_to_target_word(word):
            return word.replace(':', '')

        target_energy = self.get_target_hypothesis_energy(self.feature_table,
                                                          "d_lengthening_target_constraint_set.json", corpus,
                                                          convert_corpus_word_to_target_word_function=convert_corpus_word_to_target_word)
        # 391689

        self.simulated_annealing = SimulatedAnnealing(self.traversable_hypothesis,
                                                      target_lexicon_indicator_function=desired_lexicon_indicator_function,
                                                      sample_target_lexicon=["id", "ad"],
                                                      sample_target_outputs=["i:d", "a:d"], target_energy=target_energy)

    def test_run(self):
        self.simulated_annealing.run()

        # import cProfile
        # def fu():
        #   self.simulated_annealing.run()
        # cProfile.runctx('fu()', None, locals())

        # 97 sec
        # 75


if __name__ == '__main__':
    simulation_number = sys.argv[1]
    sys.argv = sys.argv[:1]  # leave only sys.argv[0] as sys.argv
    unittest.main()

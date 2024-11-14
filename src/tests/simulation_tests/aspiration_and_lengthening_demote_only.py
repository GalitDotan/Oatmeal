# Python2 and Python 3 compatibility:
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import random
import unittest

from src.grammar.constraint_set import ConstraintSet
from src.grammar.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing
from src.tests.log_configuration_for_testing import logger
from src.tests.otml_configuration_for_testing import configurations
from src.tests.persistence_tools import get_constraint_set_fixture, get_feature_table_fixture, get_corpus_fixture

logger.setLevel(logging.INFO)


class TestOtmlWithAspirationAndLengtheningDemoteOnly(unittest.TestCase):
    def setUp(self):
        self.feature_table = FeatureTable.load(
            get_feature_table_fixture("aspiration_and_lengthening_feature_table.json"))
        corpus = Corpus.load(get_corpus_fixture("aspiration_and_lengthening_corpus.txt"))
        self.constraint_set = ConstraintSet.load(
            get_constraint_set_fixture("aspiration_and_lengthening_demote_only_constraint_set.json"),
            self.feature_table)
        self.lexicon = Lexicon(corpus.get_words(), self.feature_table)
        self.grammar = Grammar(self.feature_table, self.constraint_set, self.lexicon)
        self.data = corpus.get_words()
        self.traversable_hypothesis = TraversableGrammarHypothesis(self.grammar, self.data)

        def function(words):
            number_of_long_vowels = sum([word.count(":") for word in words])
            number_of_aspirated_consonants = sum([word.count("h") for word in words])
            combined_number = number_of_long_vowels + number_of_aspirated_consonants
            return "number of long vowels and aspirated consonants in lexicon: {} (long vowels = {}, " \
                   "aspirated consonants = {})".format(combined_number, number_of_long_vowels,
                                                       number_of_aspirated_consonants)

        self.simulated_annealing = SimulatedAnnealing(self.traversable_hypothesis,
                                                      target_lexicon_indicator_function=function,
                                                      sample_target_lexicon=["ad", "id", "ta", "ti"],
                                                      sample_target_outputs=["a:d", "i:d", "tha", "thi"])

    run_test = True

    @unittest.skipUnless(run_test, "long running test skipped")
    def test_run(self):
        random.seed(1)
        configurations["CONSTRAINT_SET_MUTATION_WEIGHTS"] = {
            "insert_constraint": 0,
            "remove_constraint": 0,
            "demote_constraint": 1,
            "insert_feature_bundle_phonotactic_constraint": 0,
            "remove_feature_bundle_phonotactic_constraint": 0,
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

        configurations["COOLING_PARAMETER"] = 0.9995
        configurations["INITIAL_NUMBER_OF_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = 2
        configurations["MAX_FEATURE_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = 2
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 100
        configurations["MAX_NUMBER_OF_CONSTRAINTS_IN_CONSTRAINT_SET"] = 12
        configurations["RESTRICTION_ON_ALPHABET"] = True

        configurations["DEBUG_LOGGING_INTERVAL"] = 50

        number_of_steps_performed, hypothesis = self.simulated_annealing.run()


if __name__ == '__main__':
    unittest.main()

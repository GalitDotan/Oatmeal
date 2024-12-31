# Python2 and Python 3 compatibility:
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import unittest

from tests.test_logic.log_configuration_for_testing import logger
from tests.test_logic.otml_configuration_for_testing import configurations
from tests.test_logic.persistence_tools import get_constraint_set_fixture, get_feature_table_fixture, get_corpus_fixture

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing

logger.setLevel(logging.INFO)


class TestOtmlWithFaith(unittest.TestCase):
    def setUp(self):
        self.feature_table = FeatureTable.load(get_feature_table_fixture("a_b_and_cons_feature_table.json"))
        corpus = Corpus.load(get_corpus_fixture("bb_corpus.txt"))
        self.constraint_set = ConstraintSet.load(get_constraint_set_fixture("faith_constraint_set.json"),
                                                 self.feature_table)
        self.lexicon = Lexicon(corpus.get_words(), self.feature_table)
        self.grammar = Grammar(self.feature_table, self.constraint_set, self.lexicon)
        self.data = corpus.get_words()
        self.traversable_hypothesis = TraversableGrammarHypothesis(self.grammar, self.data)
        self.simulated_annealing = SimulatedAnnealing(self.traversable_hypothesis)

    run_test = True

    @unittest.skipUnless(run_test, "long running test skipped")
    def test_run(self):
        configurations["CONSTRAINT_SET_MUTATION_WEIGHTS"] = {
            "insert_constraint": 1,
            "remove_constraint": 1,
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

        configurations["DEBUG_LOGGING_INTERVAL"] = 50
        configurations["COOLING_PARAMETER"] = 0.999985
        configurations["INITIAL_NUMBER_OF_BUNDLES_IN_PHONOTACTIC_CONSTRAINT"] = 2

        number_of_steps_performed, hypothesis = self.simulated_annealing.run()


if __name__ == '__main__':
    unittest.main()

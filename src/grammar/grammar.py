# Python2 and Python 3 compatibility:
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from random import choice

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.lexicon import Word, Lexicon
from src.models.otml_configuration import settings
from src.models.transducer import Transducer
from src.utils.debug_tools import write_to_dot
from src.utils.randomization_tools import get_weighted_list
from src.utils.transducers_optimization_tools import optimize_transducer_grammar_for_word, make_optimal_paths

logger = logging.getLogger(__name__)

generation_memoization: dict[tuple[ConstraintSet, str], str] = dict()

grammar_transducers = dict()


class Grammar:
    """This class represents an Optimality Theory grammar."""

    def __init__(self, feature_table: FeatureTable, constraint_set: ConstraintSet, lexicon: Lexicon,
                 grammar_name: str = ""):
        self.feature_table: FeatureTable = feature_table
        self.constraint_set: ConstraintSet = constraint_set
        self.lexicon: Lexicon = lexicon  # all the words (probably UR) # TODO: verify if this is UR or SR
        self._grammar_name: str = grammar_name

    def __str__(self):
        return f"Grammar with [{self.constraint_set}]; and [{self.lexicon}]"

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def clear_caching():
        global generation_memoization
        generation_memoization = dict()

        global grammar_transducers
        grammar_transducers = dict()

    def get_encoding_length(self):
        """G + D:G"""
        return self.constraint_set.get_encoding_length() + self.lexicon.get_encoding_length()

    def make_mutation(self):
        """Mutate either the lexicon or the constraint set"""
        mutation_weights = [(self.lexicon, settings.lexicon_mutation_weights.sum),
                            (self.constraint_set, settings.constraint_set_mutation_weights.sum), ]

        weighted_mutatable_object_list = get_weighted_list(mutation_weights)
        object_to_mutate = choice(weighted_mutatable_object_list)
        mutation = object_to_mutate.make_mutation()
        return mutation

    def get_transducer(self):
        constraint_set_key = str(self.constraint_set)  # constraint_set is the identifier of the grammar transducer

        if constraint_set_key in grammar_transducers:
            return grammar_transducers[constraint_set_key]

        transducer = self._make_transducer()
        grammar_transducers[constraint_set_key] = transducer
        return transducer

    def _make_transducer(self):
        constraint_set_transducer = self.constraint_set.get_transducer()
        try:
            make_optimal_paths_result = make_optimal_paths(constraint_set_transducer, self.feature_table)
        except Exception as ex:
            logger.error("make_optimal_paths failed. transducer dot are being printed")
            # write_to_dot(constraint_set_transducer,"constraint_set_transducer")
            for constraint in self.constraint_set.constraints:
                pass
                # write_to_dot(constraint.get_transducer(), str(constraint))
            raise ex

        return make_optimal_paths_result

    def generate(self, word: Word):
        """
        Receives a UR and generates its SR according to this grammar.
        """
        memoization_key = (self.constraint_set, str(word))
        if memoization_key in generation_memoization:
            return generation_memoization[memoization_key]

        outputs = self._get_outputs(word, save_to_dot=False)
        generation_memoization[memoization_key] = outputs
        return outputs

    def _get_outputs(self, word: Word, save_to_dot: bool = True):
        grammar_transducer = self.get_transducer()
        word_transducer = word.get_transducer()

        if save_to_dot:  # TODO: separate writing into different function
            write_to_dot(grammar_transducer, f"{self._grammar_name}_grammar_transducer")
            write_to_dot(word_transducer, f"{self._grammar_name}_word_transducer")

        # a transducer with NULLs on inputs and JOKERs on outputs
        # a transducer with segments on inputs and sets on outputs
        intersected_transducer = Transducer.intersection(word_transducer, grammar_transducer)

        intersected_transducer.clear_dead_states()
        intersected_transducer = optimize_transducer_grammar_for_word(word, intersected_transducer)
        outputs = intersected_transducer.get_range()
        return outputs

    def get_all_outputs_grammar(self, new_string_word_list=[]):
        """
        used for testing
        """
        outputs = list()
        if new_string_word_list:
            words = [Word(word, self.feature_table) for word in new_string_word_list]
        else:
            words = self.lexicon.get_words()

        for word in words:
            outputs.extend(self._get_outputs(word, save_to_dot=False))

        return outputs

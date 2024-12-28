import logging
import os
import platform
from os.path import join

from src.grammar.constraint_set import ConstraintSet
from src.grammar.features.feature_table import FeatureTable
from src.grammar.grammar import Grammar
from src.grammar.lexicon import Lexicon
from src.models.corpus import Corpus
from src.models.otml_configuration import OtmlConfiguration, settings
from src.models.traversable_grammar_hypothesis import TraversableGrammarHypothesis
from src.simulated_annealing import SimulatedAnnealing
from tests.test_logic.persistence_tools import get_corpus_fixture


def _configure_logger(log_file_template: str, simulation_number: int):
    log_file_name = log_file_template.format(platform.node(), simulation_number)

    log_file_path = join("out", "logging", log_file_name)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s', "%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    file_log_handler = logging.FileHandler(log_file_path, mode='w')
    file_log_handler.setFormatter(file_log_formatter)
    logger.addHandler(file_log_handler)


def run_simulation(simulation_name: str,
                   simulation_number: int,
                   log_file_template: str,
                   sample_target_lexicon=None,
                   sample_target_outputs=None,
                   target_lexicon_indicator_function=None,
                   target_constraint_set_file_name=None,
                   target_lexicon_file_name=None,
                   convert_corpus_word_to_target_word_function=None,
                   initial_lexicon_file_name=None):
    config_dir = os.path.join('simulations', simulation_name)
    OtmlConfiguration.load(config_dir)

    _configure_logger(log_file_template, simulation_number)

    feature_table = FeatureTable.load(settings.features_file)
    corpus = Corpus.load(settings.corpus_file)
    constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
    lexicon = Lexicon(corpus.get_words(), feature_table)

    traversable_hypothesis = TraversableGrammarHypothesis(
        grammar=Grammar(
            feature_table,
            constraint_set, lexicon,
            grammar_name=simulation_name
        ),
        data=corpus.get_words()
    )

    keyargs_dict = {}

    if sample_target_lexicon and sample_target_outputs and target_lexicon_indicator_function:
        keyargs_dict["sample_target_lexicon"] = sample_target_lexicon
        keyargs_dict["sample_target_outputs"] = sample_target_outputs
        keyargs_dict["target_lexicon_indicator_function"] = target_lexicon_indicator_function

    if settings.target_constraints_file is not None:
        target_energy = _get_target_hypothesis_energy(feature_table, corpus,
                                                      target_lexicon_file_name,
                                                      convert_corpus_word_to_target_word_function)
        keyargs_dict["target_energy"] = target_energy

    simulated_annealing = SimulatedAnnealing(traversable_hypothesis, **keyargs_dict)
    print("Starting optimization")
    step, hypothesis = simulated_annealing.run()

    print(f'Ran {step} steps.')

    print(f'Initial hypothesis: {simulated_annealing.initial_hypothesis}')
    print(f'Final hypothesis: {simulated_annealing.current_hypothesis}')

    print("Done")


def _get_target_hypothesis_energy(feature_table, corpus,
                                  target_lexicon_file_name=None,
                                  convert_corpus_word_to_target_word_function=None):
    constraint_set = ConstraintSet.load(settings.constraints_file, feature_table)
    if target_lexicon_file_name:
        lexicon = Lexicon(get_corpus_fixture(target_lexicon_file_name), feature_table)
    elif convert_corpus_word_to_target_word_function:
        lexicon_words = [convert_corpus_word_to_target_word_function(word) for word in corpus]
        lexicon = Lexicon(lexicon_words, feature_table)
    grammar = Grammar(feature_table, constraint_set, lexicon)
    traversable_hypothesis = TraversableGrammarHypothesis(grammar, corpus)
    return traversable_hypothesis.update_energy()

import pytest

from src.grammar.lexicon import Word
from src.init_simulation import init_simulated_annealing, run_simulated_annealing_with_prints, \
    init_simulated_annealing_categories, run_simulated_annealing_with_prints_categories


@pytest.mark.parametrize(
    "simulation_name, test_words",
    [
        ("aa_bb_demote_only", {
            "bb": "bb",
            "bba": "bba",
            "aa": "aa",
            "aab": "aab",
            "aabb": "aabb"
        }),
    ]
)
def test_simulation(simulation_name: str, test_words: dict[str, str]):
    simulated_annealing = init_simulated_annealing(simulation_name)
    final_grammar = run_simulated_annealing_with_prints(simulated_annealing)
    """
    Test the MDL learner on a hypothetical language without lexical categories.

    Args:
        simulation_name (str): The name of the simulation configuration to use.
        test_words (dict[str, str]): A dictionary mapping underlying representations (URs)
            to their expected surface representations (SRs).

    Simulates a learner running the MDL algorithm on input data without lexical categories,
    evaluates whether it generalizes correctly, and prints results for verification.
    
    It is expected to NOT generalize correctly.
    This test verifies that the result hypothesis predicts UR=SR for every input.
    """
    results = []
    for ur, sr in test_words.items():
        ur_word = Word(word_string=ur, feature_table=final_grammar.feature_table)
        actual_srs = final_grammar.generate(ur_word)
        print(f'/{ur} -> [{actual_srs}]. Expected: {sr}')
        results.append(sr in actual_srs)

    print(simulated_annealing.current_hypothesis.combined_energy)
    print(f'Number of constraints in the final grammar: {len(final_grammar.constraint_set.constraints)}')
    assert all(results), f'Results: {results}'  # make sure all SRs were correct

    print("Done")


@pytest.mark.parametrize(
    "simulation_name, test_words",
    [
        ("aa_bb_demote_only_categories",
         {
             "N": {
                 "aa": "aa",
                 "aab": "aab",
                 "bb": "bab",
                 "bba": "baba",
                 "aabb": "aabab"
             },
             "V": {
                 "aa": "aba",
                 "aab": "abab",
                 "bb": "bb",
                 "bba": "bba",
                 "aabb": "ababb"
             }
         }
         ),
    ]
)
def test_simulation_categories(simulation_name: str, test_words: dict[str, dict[str, str]]):
    simulated_annealing_per_category, corpus_per_category = init_simulated_annealing_categories(simulation_name)
    final_grammars = run_simulated_annealing_with_prints_categories(simulated_annealing_per_category,
                                                                    corpus_per_category)
    """
    Test the MDL learner on a hypothetical language with lexical categories.

    Args:
        simulation_name (str): The name of the simulation configuration to use.
        test_words (dict[str, dict[str, str]]): A dictionary mapping lexical categories to dictionaries
            that map underlying representations (URs) to their expected surface representations (SRs).

    Simulates a learner running the MDL algorithm with separate cophonologies for lexical categories,
    evaluates whether it generalizes correctly for each category, and prints results for verification.
    
    It is expected to generalize correctly the two rules:
        1. bb -> bab in nouns.
        2. aa -> aba in verbs.
    """

    results: list[bool] = []
    energies: list[int] = []

    for cat, test_words_cat in test_words.items():
        for ur, sr in test_words_cat.items():
            ur_word = Word(word_string=ur, feature_table=final_grammars[cat].feature_table)
            actual_srs = final_grammars[cat].generate(ur_word)
            print(f'/{ur} -> [{actual_srs}]. Expected: {sr}')
            results.append(sr in actual_srs)
        energies.append(simulated_annealing_per_category[cat].current_hypothesis.combined_energy)

    print(f'Energies: {energies}')
    assert all(results)  # make sure all SRs were correct

    print("Done")

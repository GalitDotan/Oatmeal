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
        }),
    ]
)
def test_simulation(simulation_name: str, test_words: dict[str, str]):
    simulated_annealing = init_simulated_annealing(simulation_name)
    final_grammar = run_simulated_annealing_with_prints(simulated_annealing)

    results = []
    for ur, sr in test_words.items():
        ur_word = Word(word_string=ur, feature_table=final_grammar.feature_table)
        actual_srs = final_grammar.generate(ur_word)
        print(f'/{ur} -> [{actual_srs}]')
        results.append(sr in actual_srs)

    print(simulated_annealing.current_hypothesis.combined_energy)
    print(f'Number of constraints in the final grammar: {len(final_grammar.constraint_set.constraints)}')
    assert all(results)  # make sure all SRs were correct
    # assert len(final_grammar.constraint_set.constraints) == 0  # no constraints

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
             },
             "V": {
                 "aa": "aba",
                 "aab": "abab",
                 "bb": "bb",
                 "bba": "bba",
             }
         }
         ),
    ]
)
def test_simulation_categories(simulation_name: str, test_words: dict[str, dict[str, str]]):
    simulated_annealing_per_category, corpus_per_category = init_simulated_annealing_categories(simulation_name)
    final_grammars = run_simulated_annealing_with_prints_categories(simulated_annealing_per_category,
                                                                    corpus_per_category)

    expected: list[set[str]] = []
    actual: list[set[str]] = []
    results = []

    energies = []

    for cat, test_words_cat in test_words.items():
        for ur, sr in test_words_cat.items():
            ur_word = Word(word_string=ur, feature_table=final_grammars[cat].feature_table)
            actual.append(final_grammars[cat].generate(ur_word))
            print(f'/{ur} -> [{actual[-1]}]')
            expected.append({sr})
        energies.append(simulated_annealing_per_category[cat].current_hypothesis.combined_energy)

    print(energies)
    assert all(results)  # make sure all SRs were correct

    print("Done")

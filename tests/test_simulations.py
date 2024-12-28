import pytest

from src.grammar.lexicon import Word
from src.init_simulation import init_simulated_annealing, run_simulated_annealing_with_prints


@pytest.mark.parametrize(
    "simulation_name, test_words",
    [
        ("bb_demote_only", {
            "bb": "bab",
            "bba": "baba"
        }),
    ]
)
def test_simulation(simulation_name: str, test_words: dict[str, str]):
    simulated_annealing = init_simulated_annealing(simulation_name)
    final_grammar = run_simulated_annealing_with_prints(simulated_annealing)

    results = []
    for ur, sr in test_words.items():
        ur_word = Word(word_string=ur, feature_table=final_grammar.feature_table)
        actual = final_grammar.generate(ur_word)
        results.append(sr in actual)
    assert all(results)  # make sure all SRs were correct

    print("Done")

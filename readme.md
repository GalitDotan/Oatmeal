# Oatmeal: MDL Phonology Learner

Oatmeal is a phonological learner based on the Minimum Description Length (MDL) principle. It extends and builds upon
the original `otml` project from [TAU Computational Linguistics](https://github.com/taucompling/otml), adding support
for category-specific phonological systems and enhanced simulations.

## Simulations

The project includes two simulations for a hypothetical language with distinct phonotactic rules for nouns and verbs:

1. **Without Lexical Categories**: The learner operates without distinguishing between lexical categories (nouns and
   verbs).
    - Configuration files: `simulations/aa_bb_demote_only`

2. **With Lexical Categories**: The learner separates the input data into categories (nouns and verbs) and learns
   category-specific phonological systems.
    - Configuration files: `simulations/aa_bb_demote_only_categories`

## Tests

To verify the correctness of the simulations, the project includes test cases written using `pytest`. These tests ensure
that the learner correctly generalizes phonological rules for each scenario.

- **Test File**: `tests/test_simulations.py`

### Running the Tests

To run the tests, execute the following command in the project directory:

```bash
pytest tests/test_simulations.py
```

## Credits

Oatmeal is based on the original [otml](https://github.com/taucompling/otml) project. Special thanks to the TAU
Computational Linguistics group for providing the foundation for this work.

## License

This project is provided for educational and research purposes. Feel free to modify and extend it for your needs.

# Python2 and Python 3 compatibility:
from __future__ import absolute_import, division, print_function, unicode_literals

import textwrap

from src.grammar.lexicon import Word, get_words_from_file, parse_words_per_category_from_file
from src.models.otml_configuration import settings
from src.utils.unicode_mixin import UnicodeMixin


class Corpus(UnicodeMixin, object):

    def __init__(self, string_words):
        self.words = string_words

    def __unicode__(self):
        return f"Corpus with {len(self)} words: {self.words[:3]}..."

    def __getitem__(self, item):
        return self.words.__getitem__(item)

    def __len__(self):
        return len(self.words)

    @classmethod
    def load(cls, corpus_file_name):
        return cls.init_with_duplication(get_words_from_file(corpus_file_name))

    @classmethod
    def init_with_duplication(cls, words: list[str]):
        duplication_factor = settings.corpus_duplication_factor
        duplication_factor_int = int(duplication_factor)
        duplication_factor_fraction = duplication_factor - int(duplication_factor)

        n = len(words)
        words_after_duplication = words * duplication_factor_int
        words_after_duplication.extend(words[:int(n * duplication_factor_fraction)])

        return cls(words_after_duplication)

    @classmethod
    def load_corpus_per_category(cls, corpus_file_name) -> dict[str, "Corpus"]:
        words_per_category = parse_words_per_category_from_file(corpus_file_name)
        return {cat: cls.init_with_duplication(words) for cat, words in words_per_category.items()}

    def get_words(self):
        return self.words[:]

    def get_word_objects(self, feature_table):
        return [Word(word_string, feature_table) for word_string in self.words()]

    def print_corpus(self):
        print("Corpus ({0} words):".format(len(self)))
        lines = textwrap.wrap(" ".join([word for word in self.words]), width=80)
        for line in lines:
            print(line)

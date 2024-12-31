from io import StringIO
from random import choice


class FeatureType:
    def __init__(self, label: str, values: list[str]):
        self.label: str = label
        self.values: list[str] = values

    def get_random_value(self):
        return choice(self.values)

    def __str__(self):
        values_str_io = StringIO()
        for value in self.values:
            print(value, end=", ", file=values_str_io)
        return "FeatureType {0} with possible values: [{1}]".format(self.label, values_str_io.getvalue()[:-2])

    def __contains__(self, item):
        return item in self.values

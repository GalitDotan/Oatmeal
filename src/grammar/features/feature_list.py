from pydantic import BaseModel, Field, computed_field, model_validator

from src.exceptions import FeatureParseError
from src.grammar.features.feature import Feature


class FeatureList(BaseModel):
    features: list[Feature] = Field(allow_mutation=False)

    @computed_field
    @property
    def labels(self) -> set[str]:
        """Compute labels from features."""
        return {f.label for f in self.features}

    def __getitem__(self, key: int | str):
        if type(key) is str:
            if key in self.labels:
                return [f.values for f in self.features if f.label == key][0]
            else:
                raise KeyError(key)
        if type(key) is int:
            return self.features[key]

    def __len__(self):
        return len(self.features)

    def __iter__(self):
        return iter(self.features)

    def __contains__(self, key: str | Feature):
        if type(key) is str:
            return key in self.labels
        return key in self.features

    @model_validator(mode="after")
    def _validate_distinct(self):
        for label in self.labels:
            features = [f for f in self.features if f.label == label]
            if len(features) > 1:
                raise FeatureParseError("Feature was defined more than once", {"label": label, "definitions": features})
        return self

from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator


class FeatureValue(str, Enum):
    plus = "+"
    minus = "-"


class FeatureModel(BaseModel):
    label: str
    value: FeatureValue = Field(default=FeatureValue.minus,
                                description='A specific value',
                                exclude=True)
    values: list[FeatureValue] = Field(default=[FeatureValue.plus, FeatureValue.minus],
                                       description='All possible values',
                                       exclude=False)

    @field_validator('value', mode='before')
    @classmethod
    def validate_value(cls, value):
        if type(value) is FeatureValue:
            return value
        if type(value) is bool:
            return FeatureValue.plus if value else FeatureValue.minus
        raise ValueError(f"Invalid input of type {type(value)}. Type should be either bool or FeatureValue")

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "+" if self.value else "-"

    def __repr__(self):
        return str(self)


class FeatureListModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    label: str
    features: list[FeatureModel]

    def __hash__(self):
        return hash(self.label)


class FeaturesModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, loc_by_alias=False)
    features: list[FeatureModel] = Field(alias="feature")
    segments: dict[str, list[FeatureValue]] = Field(alias="feature_table")

    # TODO: add model validate that checks that all features exist in all segments and with the correct order

    @field_validator('segments', mode='before')
    @classmethod
    def validate_value(cls, value):
        if type(value) is dict:
            return value
        if type(value) is list:
            return {
                x.label: [feature.value for feature in x.features] for x in value
            }
        raise ValueError(f"Invalid input of type {type(value)}. Type should be either dict[str, "
                         f"list[FeatureValue]] or list[FeatureListModel]")


def save_to_file(model: BaseModel, filename) -> None:
    with open(filename + ".json", 'w', encoding="utf-8") as f:
        f.write(model.model_dump_json(by_alias=True, indent=2))

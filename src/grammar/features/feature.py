from pydantic import BaseModel


class Feature(BaseModel):
    label: str
    values: list[str]

    def __str__(self):
        return self.label

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"{self.label}: {self.values}"

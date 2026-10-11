from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


@dataclass
class IngredienteDTO:
    id: int
    nome: str
    unita: str

    @classmethod
    def from_model(cls, i):
        return cls(id=i.id, nome=i.nome, unita=i.unita_base)


class IngredienteFormDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=2, max_length=100)
    unita: Literal["g", "ml", "pz"]

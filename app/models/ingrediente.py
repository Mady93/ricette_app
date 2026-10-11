from dataclasses import dataclass


@dataclass
class Ingrediente:
    id: int
    nome: str
    unita_base: str

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class VoceDispensa:
    ingrediente_id: int
    nome: str
    unita_base: str
    quantita: Decimal


@dataclass
class Suggerimento:
    id: int
    titolo: str
    minuti: int
    difficolta: str
    totale: int
    posseduti: int

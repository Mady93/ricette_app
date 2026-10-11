from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Ricetta:
    titolo: str
    descrizione: Optional[str]
    istruzioni: str
    porzioni: int
    minuti: int
    difficolta: str
    utente_id: Optional[int] = None
    id: Optional[int] = None
    creato_il: Optional[datetime] = None


@dataclass
class RicettaSintesi:
    """Versione leggera per gli elenchi (senza istruzioni)."""
    id: int
    titolo: str
    descrizione: Optional[str]
    porzioni: int
    minuti: int
    difficolta: str


@dataclass
class RigaRicetta:
    ingrediente_id: int
    nome: str
    unita_base: str
    quantita: Decimal

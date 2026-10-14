"""Model di sola lettura per le liste dell'area admin (righe con conteggi o con l'autore)."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UtenteRiepilogo:
    id: int
    username: str
    email: str
    ruolo: str
    creato_il: Optional[datetime]
    n_ricette: int


@dataclass
class IngredienteRiepilogo:
    id: int
    nome: str
    unita_base: str
    n_ricette: int      # in quante ricette compare
    n_dispense: int     # in quante dispense degli utenti compare


@dataclass
class RicettaRiepilogo:
    id: int
    titolo: str
    autore: Optional[str]       # None = ricetta senza autore (utente eliminato)
    minuti: int
    difficolta: str
    creato_il: Optional[datetime]

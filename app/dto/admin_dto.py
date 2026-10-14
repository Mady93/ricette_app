"""DTO dell'area admin: dati verso i template e validazione del cambio ruolo."""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class CambioRuoloDTO(BaseModel):
    ruolo: Literal["utente", "admin"]


@dataclass
class StatisticheAdminDTO:
    utenti: int
    amministratori: int
    ricette: int
    ricette_senza_autore: int
    ingredienti: int
    ingredienti_inutilizzati: int       # non presenti in nessuna ricetta (quindi eliminabili)


@dataclass
class UtenteAdminDTO:
    id: int
    username: str
    email: str
    ruolo: str
    creato_il: Optional[datetime]
    n_ricette: int

    @property
    def is_admin(self) -> bool:
        return self.ruolo == "admin"

    @classmethod
    def from_model(cls, u):
        return cls(u.id, u.username, u.email, u.ruolo, u.creato_il, u.n_ricette)


@dataclass
class IngredienteAdminDTO:
    id: int
    nome: str
    unita: str
    n_ricette: int
    n_dispense: int

    @property
    def eliminabile(self) -> bool:
        return self.n_ricette == 0

    @property
    def unita_modificabile(self) -> bool:
        return self.n_ricette == 0 and self.n_dispense == 0

    @classmethod
    def from_model(cls, i):
        return cls(i.id, i.nome, i.unita_base, i.n_ricette, i.n_dispense)


@dataclass
class RicettaAdminDTO:
    id: int
    titolo: str
    autore: Optional[str]
    minuti: int
    difficolta: str
    creato_il: Optional[datetime]

    @classmethod
    def from_model(cls, r):
        return cls(r.id, r.titolo, r.autore, r.minuti, r.difficolta, r.creato_il)

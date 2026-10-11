from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Utente:
    """Model: dati scambiati tra service e repository."""
    username: str
    email: str
    password_hash: str
    ruolo: str = "utente"
    id: Optional[int] = None
    creato_il: Optional[datetime] = None

    @property
    def is_authenticated(self) -> bool:
        return True


class UtenteAnonimo:
    """Null Object Pattern per utenti non autenticati."""
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_active(self) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return True

    @property
    def username(self) -> str:
        return ""
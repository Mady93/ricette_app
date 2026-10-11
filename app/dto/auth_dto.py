import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


class RegistrazioneDTO(BaseModel):
    """DTO di input: le regole stanno qui, come con @Valid in Spring."""
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    conferma_password: str = Field(max_length=128)

    @field_validator("username", "email", mode="before")
    @classmethod
    def _toglie_spazi(cls, v):
        return v.strip() if isinstance(v, str) else v      # la password NON si tocca

    @field_validator("username")
    @classmethod
    def _username_valido(cls, v):
        if not _USERNAME_RE.match(v):
            raise ValueError("Usa solo lettere, numeri o underscore.")
        return v

    @field_validator("email")
    @classmethod
    def _email_normalizzata(cls, v):
        if len(v) > 150:
            raise ValueError("L'email è troppo lunga.")
        return v.lower()

    @field_validator("password")
    @classmethod
    def _password_robusta(cls, v, info: ValidationInfo):
        if not (any(c.isalpha() for c in v) and any(c.isdigit() for c in v)):
            raise ValueError("La password deve contenere almeno una lettera e un numero.")
        username = info.data.get("username")
        if username and v.lower() == username.lower():
            raise ValueError("La password non può coincidere con lo username.")
        return v

    @field_validator("conferma_password")
    @classmethod
    def _password_uguali(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Le due password non coincidono.")
        return v


class LoginDTO(BaseModel):
    identificativo: str = Field(min_length=1, max_length=150)      # username oppure email
    password: str = Field(min_length=1, max_length=128)

    @field_validator("identificativo", mode="before")
    @classmethod
    def _toglie_spazi(cls, v):
        return v.strip() if isinstance(v, str) else v


@dataclass
class UtenteDTO:
    """DTO di output verso il controller: mai l'hash della password."""
    id: int
    username: str
    email: str
    ruolo: str
    creato_il: Optional[datetime] = None

    @property
    def is_authenticated(self) -> bool:
        return True  # Essendo un DTO di un utente caricato, è sempre autenticato

    @classmethod
    def from_model(cls, u):
        return cls(
            id=u.id, 
            username=u.username, 
            email=u.email,
            ruolo=u.ruolo, 
            creato_il=u.creato_il
        )

class AggiornaProfiloDTO(BaseModel):
    """DTO per la modifica del profilo."""
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr

    @field_validator("username", "email", mode="before")
    @classmethod
    def _toglie_spazi(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("username")
    @classmethod
    def _username_valido(cls, v):
        if not _USERNAME_RE.match(v):
            raise ValueError("Usa solo lettere, numeri o underscore.")
        return v

    @field_validator("email")
    @classmethod
    def _email_normalizzata(cls, v):
        if len(v) > 150:
            raise ValueError("L'email è troppo lunga.")
        return v.lower()
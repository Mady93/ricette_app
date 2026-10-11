"""Ponte tra Pydantic e le eccezioni dell'applicazione (il nostro @Valid)."""
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.exceptions import ValidazioneError

T = TypeVar("T", bound=BaseModel)

_MSG_RIGA = "Ogni riga ha bisogno di un ingrediente e di una quantità maggiore di 0."


def valida(modello: Type[T], dati: dict) -> T:
    """Costruisce il DTO oppure lancia ValidazioneError({campo: messaggio})."""
    try:
        return modello.model_validate(dati)
    except ValidationError as e:
        raise ValidazioneError(errori_da_pydantic(e)) from None


def errori_da_pydantic(e: ValidationError) -> dict:
    errori = {}
    for err in e.errors():
        loc = err["loc"]
        campo = "ingredienti" if loc and loc[0] == "righe" else (str(loc[0]) if loc else "generale")
        errori.setdefault(campo, _messaggio(err))        # un solo messaggio per campo
    return errori


def _messaggio(err: dict) -> str:
    tipo, loc, ctx = err["type"], err["loc"], err.get("ctx") or {}

    if loc and loc[0] == "righe":
        if len(loc) == 1 and tipo == "too_short":
            return "Aggiungi almeno un ingrediente."
        if len(loc) == 1 and tipo == "value_error":
            return err["msg"].removeprefix("Value error, ")
        return _MSG_RIGA

    if tipo == "value_error":
        msg = err["msg"].removeprefix("Value error, ")
        return "Inserisci un indirizzo email valido." if "email address" in msg else msg

    traduzioni = {
        "string_too_short": lambda: f"Almeno {ctx.get('min_length')} caratteri.",
        "string_too_long": lambda: f"Al massimo {ctx.get('max_length')} caratteri.",
        "greater_than_equal": lambda: f"Il valore minimo è {ctx.get('ge')}.",
        "less_than_equal": lambda: f"Il valore massimo è {ctx.get('le')}.",
        "greater_than": lambda: f"Deve essere maggiore di {ctx.get('gt')}.",
        "int_parsing": lambda: "Inserisci un numero intero.",
        "int_from_float": lambda: "Inserisci un numero intero.",
        "int_type": lambda: "Inserisci un numero intero.",
        "decimal_parsing": lambda: "Inserisci un numero valido (max 2 decimali).",
        "decimal_type": lambda: "Inserisci un numero valido (max 2 decimali).",
        "decimal_max_places": lambda: "Inserisci un numero valido (max 2 decimali).",
        "decimal_max_digits": lambda: "Inserisci un numero valido (max 2 decimali).",
        "decimal_whole_digits": lambda: "Inserisci un numero valido (max 2 decimali).",
        "literal_error": lambda: "Scegli un valore valido.",
        "missing": lambda: "Campo obbligatorio.",
        "string_type": lambda: "Valore non valido.",
    }
    return traduzioni.get(tipo, lambda: err["msg"])()

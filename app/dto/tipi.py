"""Tipi riusabili per i DTO."""

from decimal import Decimal

from typing import Annotated

from pydantic import BeforeValidator, Field


def _virgola_in_punto(value: object) -> object:

    """Converte il separatore decimale italiano in quello standard."""

    if isinstance(value, str):

        return value.strip().replace(",", ".")

    return value


Quantita = Annotated[

    Decimal,

    BeforeValidator(_virgola_in_punto),

    Field(

        gt=0,

        decimal_places=2,

    ),

]

QuantitaDispensa = Annotated[
    Quantita,
    Field(le=1_000_000),
]

QuantitaIngredienteRicetta = Annotated[
    Quantita,
    Field(le=100_000),
]
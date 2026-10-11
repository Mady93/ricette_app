from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field

from app.dto.tipi import QuantitaDispensa


class DispensaFormDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ingrediente_id: int = Field(ge=1, le=2_147_483_647)
    quantita: QuantitaDispensa


@dataclass
class VoceDispensaDTO:
    ingrediente_id: int
    nome: str
    unita: str
    quantita: float


@dataclass
class SuggerimentoDTO:
    id: int
    titolo: str
    minuti: int
    difficolta: str
    totale: int
    posseduti: int
    percentuale: int


@dataclass
class VoceSpesaDTO:
    nome: str
    unita: str
    quantita: float
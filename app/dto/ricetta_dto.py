from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.dto.tipi import QuantitaIngredienteRicetta


# ---------------- input validato (Pydantic) ----------------
class RigaIngredienteDTO(BaseModel):
    ingrediente_id: int = Field(ge=1, le=2_147_483_647)
    quantita: QuantitaIngredienteRicetta


class RicettaFormDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titolo: str = Field(min_length=3, max_length=150)
    descrizione: str = Field(default="", max_length=1000)
    istruzioni: str = Field(min_length=10, max_length=10000)
    porzioni: int = Field(ge=1, le=50)
    minuti: int = Field(ge=1, le=1440)
    difficolta: Literal["facile", "media", "difficile"]
    righe: List[RigaIngredienteDTO] = Field(min_length=1, max_length=60)

    @field_validator("righe")
    @classmethod
    def _senza_duplicati(cls, v):
        ids = [r.ingrediente_id for r in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Un ingrediente è ripetuto.")
        return v


# ---------------- dati grezzi per ripopolare il form ----------------
@dataclass
class RicettaFormDati:
    """Quello che l'utente ha scritto, tale e quale (stringhe), da rimostrare dopo un errore."""
    titolo: str = ""
    descrizione: str = ""
    istruzioni: str = ""
    porzioni: str = "4"
    minuti: str = "30"
    difficolta: str = "facile"
    righe: List[Tuple[str, str]] = field(default_factory=list)      # (ingrediente_id, quantita)

    @classmethod
    def da_form(cls, form):
        righe = list(zip(form.getlist("ingrediente_id"), form.getlist("quantita")))
        return cls(
            titolo=form.get("titolo", ""),
            descrizione=form.get("descrizione", ""),
            istruzioni=form.get("istruzioni", ""),
            porzioni=form.get("porzioni", ""),
            minuti=form.get("minuti", ""),
            difficolta=form.get("difficolta", ""),
            righe=righe[:60],
        )

    def come_dict(self):
        """Per Pydantic: scarta le righe del tutto vuote del form."""
        return {
            "titolo": self.titolo, "descrizione": self.descrizione, "istruzioni": self.istruzioni,
            "porzioni": self.porzioni, "minuti": self.minuti, "difficolta": self.difficolta,
            "righe": [{"ingrediente_id": i, "quantita": q} for i, q in self.righe if i.strip() or q.strip()],
        }

    def righe_complete(self, minimo=10):
        n = max(minimo, len(self.righe) + 2)
        return list(self.righe) + [("", "")] * (n - len(self.righe))


# ---------------- output (dataclass semplici) ----------------
@dataclass
class RicettaListaDTO:
    id: int
    titolo: str
    descrizione: str
    porzioni: int
    minuti: int
    difficolta: str

    @classmethod
    def from_model(cls, r):
        return cls(r.id, r.titolo, r.descrizione or "", r.porzioni, r.minuti, r.difficolta)


@dataclass
class PaginaDTO:
    items: list
    pagina: int
    pagine: int
    totale: int


@dataclass
class RigaDettaglioDTO:
    ingrediente_id: int
    nome: str
    unita: str
    quantita: float
    posseduta: Optional[float] = None     # None = utente non loggato
    mancante: Optional[float] = None


@dataclass
class RicettaDettaglioDTO:
    id: int
    utente_id: Optional[int]
    titolo: str
    descrizione: str
    istruzioni: str
    porzioni_base: int
    porzioni: int
    minuti: int
    difficolta: str
    righe: List[RigaDettaglioDTO]
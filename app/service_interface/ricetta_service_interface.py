from abc import ABC, abstractmethod
from typing import List, Optional

from app.dto.auth_dto import UtenteDTO
from app.dto.ingrediente_dto import IngredienteDTO
from app.dto.ricetta_dto import PaginaDTO, RicettaDettaglioDTO, RicettaFormDati, RicettaFormDTO


class RicettaServiceInterface(ABC):
    @abstractmethod
    def elenco(self, q: str, difficolta: Optional[str], max_minuti: Optional[int], pagina: int, per_page: int = 5) -> PaginaDTO: ...

    @abstractmethod
    def dettaglio(self, ricetta_id: int, porzioni: Optional[int], utente_id: Optional[int]) -> RicettaDettaglioDTO: ...

    @abstractmethod
    def crea(self, utente_id: int, dto: RicettaFormDTO) -> int: ...

    @abstractmethod
    def per_modifica(self, utente: UtenteDTO, ricetta_id: int) -> RicettaFormDati: ...

    @abstractmethod
    def modifica(self, utente: UtenteDTO, ricetta_id: int, dto: RicettaFormDTO) -> None: ...

    @abstractmethod
    def elimina(self, utente: UtenteDTO, ricetta_id: int) -> None: ...

    @abstractmethod
    def ingredienti_disponibili(self) -> List[IngredienteDTO]: ...

    @abstractmethod
    def esistono_ricette(self) -> bool: ...
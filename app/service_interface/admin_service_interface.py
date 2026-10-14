from abc import ABC, abstractmethod
from typing import List

from app.dto.admin_dto import (
    CambioRuoloDTO, IngredienteAdminDTO, StatisticheAdminDTO, UtenteAdminDTO,
)
from app.dto.auth_dto import UtenteDTO
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.ricetta_dto import PaginaDTO


class AdminServiceInterface(ABC):
    """Contratto delle operazioni riservate agli amministratori.

    Il primo parametro e' sempre l'utente che agisce: ogni metodo verifica che sia admin.
    """

    @abstractmethod
    def statistiche(self, admin: UtenteDTO) -> StatisticheAdminDTO: ...

    # ---- utenti ----
    @abstractmethod
    def utenti(self, admin: UtenteDTO) -> List[UtenteAdminDTO]: ...

    @abstractmethod
    def cambia_ruolo(self, admin: UtenteDTO, utente_id: int, dto: CambioRuoloDTO) -> UtenteDTO: ...

    @abstractmethod
    def elimina_utente(self, admin: UtenteDTO, utente_id: int) -> UtenteDTO: ...

    # ---- ingredienti ----
    @abstractmethod
    def ingredienti(self, admin: UtenteDTO) -> List[IngredienteAdminDTO]: ...

    @abstractmethod
    def ingrediente(self, admin: UtenteDTO, ingrediente_id: int) -> IngredienteAdminDTO: ...

    @abstractmethod
    def modifica_ingrediente(self, admin: UtenteDTO, ingrediente_id: int, dto: IngredienteFormDTO) -> None: ...

    @abstractmethod
    def elimina_ingrediente(self, admin: UtenteDTO, ingrediente_id: int) -> str: ...

    # ---- ricette ----
    @abstractmethod
    def ricette(self, admin: UtenteDTO, q: str, solo_senza_autore: bool, pagina: int) -> PaginaDTO: ...

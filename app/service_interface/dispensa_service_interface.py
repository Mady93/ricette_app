from abc import ABC, abstractmethod
from typing import List, Optional

from app.dto.dispensa_dto import DispensaFormDTO, SuggerimentoDTO, VoceDispensaDTO, VoceSpesaDTO


class DispensaServiceInterface(ABC):
    @abstractmethod
    def elenco(self, utente_id: int) -> List[VoceDispensaDTO]: ...

    @abstractmethod
    def imposta(self, utente_id: int, dto: DispensaFormDTO) -> None: ...

    @abstractmethod
    def rimuovi(self, utente_id: int, ingrediente_id: int) -> None: ...

    @abstractmethod
    def cosa_posso_cucinare(self, utente_id: int) -> List[SuggerimentoDTO]: ...

    @abstractmethod
    def lista_spesa(self, utente_id: int, ricetta_id: int, porzioni: Optional[int]) -> List[VoceSpesaDTO]: ...

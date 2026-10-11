from abc import ABC, abstractmethod
from typing import List

from app.dto.ingrediente_dto import IngredienteDTO, IngredienteFormDTO


class IngredienteServiceInterface(ABC):
    @abstractmethod
    def elenco(self) -> List[IngredienteDTO]: ...

    @abstractmethod
    def crea(self, dto: IngredienteFormDTO) -> int: ...

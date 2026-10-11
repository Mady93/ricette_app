import mysql.connector

from app.dto.ingrediente_dto import IngredienteDTO, IngredienteFormDTO
from app.exceptions import ConflittoError
from app.repositories.ingrediente_repository import IngredienteRepository
from app.service_interface.ingrediente_service_interface import IngredienteServiceInterface


class IngredienteService(IngredienteServiceInterface):
    def __init__(self, repo: IngredienteRepository):
        self._repo = repo

    def elenco(self):
        return [IngredienteDTO.from_model(i) for i in self._repo.find_all()]

    def crea(self, dto: IngredienteFormDTO) -> int:
        if self._repo.exists_by_nome(dto.nome):
            raise ConflittoError("Esiste già un ingrediente con questo nome.")
        try:
            return self._repo.save(dto.nome, dto.unita)
        except mysql.connector.IntegrityError:
            raise ConflittoError("Esiste già un ingrediente con questo nome.")

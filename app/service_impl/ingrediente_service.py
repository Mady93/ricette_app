import csv
import io
import mysql.connector

from app.dto.ingrediente_dto import IngredienteDTO, IngredienteFormDTO
from app.exceptions import ConflittoError, ValidazioneError
from app.dto.validazione import valida
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

    def importa_da_csv(self, file_stream):
        # Assicura di partire dall'inizio dello stream del file
        if hasattr(file_stream, 'seek'):
            file_stream.seek(0)
            
        # Legge lo stream del file caricato dall'admin
        stream = io.TextIOWrapper(file_stream, encoding="utf-8")
        reader = csv.DictReader(stream)
        
        # VALIDAZIONE STRUTTURA: Controlla che le colonne obbligatorie esistano nel CSV
        colonne_richieste = {"nome", "unita"}
        if not reader.fieldnames or not colonne_richieste.issubset(set(reader.fieldnames)):
            raise ValidazioneError({"file": "Il file CSV non è valido per gli ingredienti. Colonne obbligatorie mancanti: nome, unita."})
        
        inseriti = 0
        saltati = 0
        
        for riga in reader:
            dati = {
                "nome": riga.get("nome", "").strip(),
                "unita": riga.get("unita", "").strip()
            }
            if not dati["nome"] and not dati["unita"]:
                continue
                
            dto_validato = valida(IngredienteFormDTO, dati)
            try:
                self.crea(dto_validato)
                inseriti += 1
            except ConflittoError:
                saltati += 1
                
        return inseriti, saltati

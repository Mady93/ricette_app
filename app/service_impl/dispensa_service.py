from app.dto.dispensa_dto import DispensaFormDTO, SuggerimentoDTO, VoceDispensaDTO, VoceSpesaDTO
from app.exceptions import ValidazioneError
from app.repositories.dispensa_repository import DispensaRepository
from app.repositories.ingrediente_repository import IngredienteRepository
from app.service_interface.dispensa_service_interface import DispensaServiceInterface
from app.service_interface.ricetta_service_interface import RicettaServiceInterface

MAX_SUGGERIMENTI = 24


class DispensaService(DispensaServiceInterface):
    def __init__(self, dispensa: DispensaRepository, ingredienti: IngredienteRepository,
                 ricette: RicettaServiceInterface):
        self._dispensa = dispensa
        self._ingredienti = ingredienti
        self._ricette = ricette

    def elenco(self, utente_id):
        return [VoceDispensaDTO(v.ingrediente_id, v.nome, v.unita_base, float(v.quantita))
                for v in self._dispensa.find_by_utente(utente_id)]

    def imposta(self, utente_id, dto: DispensaFormDTO):
        if not self._ingredienti.find_ids_esistenti([dto.ingrediente_id]):
            raise ValidazioneError({"ingrediente_id": "Scegli un ingrediente dalla lista."})
        self._dispensa.upsert(utente_id, dto.ingrediente_id, dto.quantita)

    def rimuovi(self, utente_id, ingrediente_id):
        self._dispensa.delete(utente_id, ingrediente_id)

    def cosa_posso_cucinare(self, utente_id):
        return [SuggerimentoDTO(s.id, s.titolo, s.minuti, s.difficolta, s.totale, s.posseduti,
                                round(100 * s.posseduti / s.totale))
                for s in self._dispensa.suggerimenti(utente_id, MAX_SUGGERIMENTI)]

    def lista_spesa(self, utente_id, ricetta_id, porzioni):
        det = self._ricette.dettaglio(ricetta_id, porzioni, utente_id)
        return [VoceSpesaDTO(r.nome, r.unita, r.mancante) for r in det.righe if r.mancante and r.mancante > 0]

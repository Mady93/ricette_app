from dataclasses import dataclass
from math import ceil

from app.dto.dispensa_dto import DispensaFormDTO, SuggerimentoDTO, VoceDispensaDTO, VoceSpesaDTO
from app.exceptions import ValidazioneError
from app.repositories.dispensa_repository import DispensaRepository
from app.repositories.ingrediente_repository import IngredienteRepository
from app.service_interface.dispensa_service_interface import DispensaServiceInterface
from app.service_interface.ricetta_service_interface import RicettaServiceInterface

MAX_SUGGERIMENTI = 24        # usato dalla home (ne mostra i primi 5)
MAX_RISULTATI = 2000         # tetto di sicurezza per la pagina "Cosa cucino?"
VALORI_PER_PAGINA = {5, 11, 23, 47, 97}
PER_PAGINA_DEFAULT = 11


@dataclass(frozen=True)
class PaginaSuggerimenti:
    """Una pagina di suggerimenti, con filtri normalizzati e conteggi per gruppo."""
    items: list
    pagina: int
    pagine: int
    totale: int
    per_page: int
    primo: int               # numero della prima ricetta mostrata (0 se non ce ne sono)
    ultimo: int              # numero dell'ultima ricetta mostrata
    gruppi: tuple            # ricette per ingredienti mancanti: (0, 1, 2, 3 o più)
    difficolta: str          # "" = tutte
    max_minuti: str          # "" = nessun limite
    max_mancanti: str        # "" = qualsiasi


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
        return [self._dto(s) for s in self._dispensa.suggerimenti(utente_id, MAX_SUGGERIMENTI)]

    def suggerimenti_pagina(self, utente_id, difficolta, max_minuti, max_mancanti, pagina, per_page):
        """Suggerimenti filtrati, raggruppati per ingredienti mancanti e divisi in pagine."""
        if difficolta not in ("facile", "media", "difficile"):
            difficolta = None
        if max_minuti is not None and not 1 <= max_minuti <= 1440:
            max_minuti = None
        if max_mancanti not in (0, 1, 2):
            max_mancanti = None
        if per_page not in VALORI_PER_PAGINA:
            per_page = PER_PAGINA_DEFAULT

        tutti = [self._dto(s) for s in self._dispensa.suggerimenti(utente_id, MAX_RISULTATI)]
        filtrati = [
            x for x in tutti
            if (difficolta is None or x.difficolta == difficolta)
            and (max_minuti is None or x.minuti <= max_minuti)
            and (max_mancanti is None or x.totale - x.posseduti <= max_mancanti)
        ]
        # prima quelle a cui manca meno; a parità, la percentuale più alta
        filtrati.sort(key=lambda x: (min(x.totale - x.posseduti, 3), -x.percentuale, x.totale, x.titolo))

        gruppi = [0, 0, 0, 0]
        for x in filtrati:
            gruppi[min(x.totale - x.posseduti, 3)] += 1

        totale = len(filtrati)
        pagine = max(1, ceil(totale / per_page))
        pagina = min(max(pagina or 1, 1), pagine)
        inizio = (pagina - 1) * per_page
        return PaginaSuggerimenti(
            items=filtrati[inizio:inizio + per_page], pagina=pagina, pagine=pagine, totale=totale,
            per_page=per_page, primo=inizio + 1 if totale else 0, ultimo=min(inizio + per_page, totale),
            gruppi=tuple(gruppi), difficolta=difficolta or "",
            max_minuti="" if max_minuti is None else str(max_minuti),
            max_mancanti="" if max_mancanti is None else str(max_mancanti),
        )

    @staticmethod
    def _dto(s):
        return SuggerimentoDTO(s.id, s.titolo, s.minuti, s.difficolta, s.totale, s.posseduti,
                               round(100 * s.posseduti / s.totale))

    def lista_spesa(self, utente_id, ricetta_id, porzioni):
        det = self._ricette.dettaglio(ricetta_id, porzioni, utente_id)
        return [VoceSpesaDTO(r.nome, r.unita, r.mancante) for r in det.righe if r.mancante and r.mancante > 0]
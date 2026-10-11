from decimal import Decimal
from math import ceil
from typing import Optional

from app.dto.auth_dto import UtenteDTO
from app.dto.ingrediente_dto import IngredienteDTO
from app.dto.ricetta_dto import (
    PaginaDTO, RicettaDettaglioDTO, RicettaFormDati, RicettaFormDTO, RicettaListaDTO, RigaDettaglioDTO,
)
from app.exceptions import NonAutorizzatoError, RisorsaNonTrovataError, ValidazioneError
from app.models.ricetta import Ricetta
from app.repositories.dispensa_repository import DispensaRepository
from app.repositories.ingrediente_repository import IngredienteRepository
from app.repositories.ricetta_repository import RicettaRepository
from app.service_interface.ricetta_service_interface import RicettaServiceInterface

# Valori consentiti per gli elementi per pagina (numeri primi)
VALORI_PER_PAGINA = {5, 11, 23, 47, 97}


class RicettaService(RicettaServiceInterface):
    def __init__(self, ricette: RicettaRepository, ingredienti: IngredienteRepository,
                 dispensa: DispensaRepository):
        self._ricette = ricette
        self._ingredienti = ingredienti
        self._dispensa = dispensa

    # ---------- lettura ----------
    def elenco(self, q, difficolta, max_minuti, pagina, per_page=5):
        q = (q or "").strip()[:100]
        if difficolta not in ("facile", "media", "difficile"):
            difficolta = None
        if max_minuti is not None and not 1 <= max_minuti <= 1440:
            max_minuti = None
        
        # Validazione del per_page scelto dall'utente (default a 5 se non valido)
        if per_page not in VALORI_PER_PAGINA:
            per_page = 5

        totale = self._ricette.conta(q, difficolta, max_minuti)
        pagine = max(1, ceil(totale / per_page))
        pagina = min(max(pagina or 1, 1), pagine)
        items = self._ricette.cerca(q, difficolta, max_minuti, per_page, (pagina - 1) * per_page)
        return PaginaDTO([RicettaListaDTO.from_model(r) for r in items], pagina, pagine, totale)

    def dettaglio(self, ricetta_id, porzioni, utente_id):
        r = self._carica(ricetta_id)
        n = porzioni if porzioni and 1 <= porzioni <= 50 else r.porzioni
        fattore = Decimal(n) / Decimal(r.porzioni)
        possedute = self._dispensa.possedute_per_ricetta(utente_id, ricetta_id) if utente_id else {}
        righe = []
        for x in self._ricette.righe_di(ricetta_id):
            serve = (x.quantita * fattore).quantize(Decimal("0.01"))
            if utente_id:
                ha = possedute.get(x.ingrediente_id, Decimal(0))
                righe.append(RigaDettaglioDTO(x.ingrediente_id, x.nome, x.unita_base, float(serve),
                                              float(ha), float(max(serve - ha, Decimal(0)))))
            else:
                righe.append(RigaDettaglioDTO(x.ingrediente_id, x.nome, x.unita_base, float(serve)))
        return RicettaDettaglioDTO(r.id, r.utente_id, r.titolo, r.descrizione or "", r.istruzioni,
                                   r.porzioni, n, r.minuti, r.difficolta, righe)

    def ingredienti_disponibili(self):
        return [IngredienteDTO.from_model(i) for i in self._ingredienti.find_all()]

    # ---------- scrittura ----------
    def crea(self, utente_id, dto):
        ricetta, righe = self._prepara(dto)
        ricetta.utente_id = utente_id
        return self._ricette.save(ricetta, righe)

    def per_modifica(self, utente, ricetta_id):
        r = self._carica(ricetta_id)
        self._controlla_proprietario(utente, r)
        righe = [(str(x.ingrediente_id), format(x.quantita.normalize(), "f")) for x in self._ricette.righe_di(ricetta_id)]
        return RicettaFormDati(r.titolo, r.descrizione or "", r.istruzioni, str(r.porzioni),
                                str(r.minuti), r.difficolta, righe)

    def modifica(self, utente, ricetta_id, dto):
        esistente = self._carica(ricetta_id)
        self._controlla_proprietario(utente, esistente)
        ricetta, righe = self._prepara(dto)
        ricetta.id = ricetta_id
        self._ricette.update(ricetta, righe)

    def elimina(self, utente, ricetta_id):
        r = self._carica(ricetta_id)
        self._controlla_proprietario(utente, r)
        self._ricette.delete(ricetta_id)

    # ---------- interne ----------
    def _carica(self, ricetta_id):
        r = self._ricette.find_by_id(ricetta_id)
        if r is None:
            raise RisorsaNonTrovataError("Ricetta non trovata.")
        return r

    @staticmethod
    def _controlla_proprietario(utente: UtenteDTO, r: Ricetta):
        if utente.ruolo != "admin" and r.utente_id != utente.id:
            raise NonAutorizzatoError("Puoi modificare solo le tue ricette.")

    def _prepara(self, dto: RicettaFormDTO):
        """Il DTO e' gia' valido nella forma: qui si controllano le regole che richiedono il DB."""
        ids = [r.ingrediente_id for r in dto.righe]
        if len(self._ingredienti.find_ids_esistenti(ids)) != len(ids):
            raise ValidazioneError({"ingredienti": "Uno degli ingredienti scelti non esiste."})
        ricetta = Ricetta(dto.titolo, dto.descrizione or None, dto.istruzioni,
                          dto.porzioni, dto.minuti, dto.difficolta)
        return ricetta, [(r.ingrediente_id, r.quantita) for r in dto.righe]

    def esistono_ricette(self) -> bool:
        return self._ricette.conta("", None, None) > 0
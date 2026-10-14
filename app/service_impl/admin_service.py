from math import ceil

import mysql.connector

from app.dto.admin_dto import (
    CambioRuoloDTO, IngredienteAdminDTO, RicettaAdminDTO, StatisticheAdminDTO, UtenteAdminDTO,
)
from app.dto.auth_dto import UtenteDTO
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.ricetta_dto import PaginaDTO
from app.exceptions import ConflittoError, NonAutorizzatoError, RisorsaNonTrovataError
from app.repositories.ingrediente_repository import IngredienteRepository
from app.repositories.ricetta_repository import RicettaRepository
from app.repositories.utente_repository import UtenteRepository
from app.service_interface.admin_service_interface import AdminServiceInterface

RICETTE_PER_PAGINA = 20


def _conta(n: int, singolare: str, plurale: str) -> str:
    return f"{n} {singolare if n == 1 else plurale}"


class AdminService(AdminServiceInterface):
    """Regole di business dell'area admin. Il controller non decide nulla da solo."""

    def __init__(self, utenti: UtenteRepository, ricette: RicettaRepository,
                 ingredienti: IngredienteRepository):
        self._utenti = utenti
        self._ricette = ricette
        self._ingredienti = ingredienti

    # ---------- permessi ----------
    @staticmethod
    def _solo_admin(admin: UtenteDTO) -> None:
        """Seconda barriera dopo il decorator @admin_required: il service non si fida del chiamante."""
        if admin is None or admin.ruolo != "admin":
            raise NonAutorizzatoError()

    # ---------- dashboard ----------
    def statistiche(self, admin):
        self._solo_admin(admin)
        return StatisticheAdminDTO(
            utenti=self._utenti.conta(),
            amministratori=self._utenti.conta_admin(),
            ricette=self._ricette.conta_admin("", False),
            ricette_senza_autore=self._ricette.conta_admin("", True),
            ingredienti=self._ingredienti.conta(),
            ingredienti_inutilizzati=self._ingredienti.conta_inutilizzati(),
        )

    # ---------- utenti ----------
    def utenti(self, admin):
        self._solo_admin(admin)
        return [UtenteAdminDTO.from_model(u) for u in self._utenti.find_all_con_ricette()]

    def cambia_ruolo(self, admin, utente_id, dto: CambioRuoloDTO):
        self._solo_admin(admin)
        
        # Forza utente_id a intero per evitare problemi di tipo con i form HTML ("1" vs 1)
        utente_id = int(utente_id)
        
        # 1. IL SUPREMO È INTOCCABILE DA CHIUNQUE (Mettilo SEMPRE per primo!)
        if utente_id == 1:
            raise ConflittoError("Non puoi modificare il ruolo del Super-Admin principale (ID 1).")
        
        # 2. Non puoi cambiare il tuo stesso ruolo
        if utente_id == admin.id:
            raise ConflittoError("Non puoi cambiare il tuo stesso ruolo.")

        utente = self._carica_utente(utente_id)
        self._utenti.update_ruolo(utente_id, dto.ruolo)
        utente.ruolo = dto.ruolo
        return UtenteDTO.from_model(utente)

    def elimina_utente(self, admin, utente_id):
        self._solo_admin(admin)
        
        # Forza utente_id a intero
        utente_id = int(utente_id)
        
        # 1. IL SUPREMO È INTOCCABILE DA CHIUNQUE
        if utente_id == 1:
            raise ConflittoError("Non puoi eliminare il Super-Admin principale (ID 1).")
            
        # 2. Non puoi eliminare te stesso
        if utente_id == admin.id:
            raise ConflittoError("Non puoi eliminare il tuo stesso account.")

        utente = self._carica_utente(utente_id)
        self._utenti.delete(utente_id)
        return UtenteDTO.from_model(utente)

    def _carica_utente(self, utente_id):
        utente = self._utenti.find_by_id(utente_id)
        if utente is None:
            raise RisorsaNonTrovataError("Utente non trovato.")
        return utente

    # ---------- ingredienti ----------
    def ingredienti(self, admin):
        self._solo_admin(admin)
        return [IngredienteAdminDTO.from_model(i) for i in self._ingredienti.find_all_con_utilizzi()]

    def ingrediente(self, admin, ingrediente_id):
        self._solo_admin(admin)
        ing = self._carica_ingrediente(ingrediente_id)
        n_ricette, n_dispense = self._ingredienti.utilizzi(ingrediente_id)
        return IngredienteAdminDTO(ing.id, ing.nome, ing.unita_base, n_ricette, n_dispense)

    def modifica_ingrediente(self, admin, ingrediente_id, dto: IngredienteFormDTO):
        self._solo_admin(admin)
        ing = self._carica_ingrediente(ingrediente_id)
        if self._ingredienti.exists_by_nome_escluso(dto.nome, ingrediente_id):
            raise ConflittoError("Esiste già un ingrediente con questo nome.")
        if dto.unita != ing.unita_base:
            # Cambiare g -> pz con le quantita' gia' salvate le renderebbe senza senso.
            n_ricette, n_dispense = self._ingredienti.utilizzi(ingrediente_id)
            if n_ricette or n_dispense:
                raise ConflittoError(
                    f"Non puoi cambiare l'unità di «{ing.nome}»: è usato in "
                    f"{_conta(n_ricette, 'ricetta', 'ricette')} e in "
                    f"{_conta(n_dispense, 'dispensa', 'dispense')}, e le quantità già salvate "
                    "diventerebbero sbagliate."
                )
        try:
            self._ingredienti.update(ingrediente_id, dto.nome, dto.unita)
        except mysql.connector.IntegrityError:
            raise ConflittoError("Esiste già un ingrediente con questo nome.")

    def elimina_ingrediente(self, admin, ingrediente_id):
        self._solo_admin(admin)
        ing = self._carica_ingrediente(ingrediente_id)
        n_ricette, _ = self._ingredienti.utilizzi(ingrediente_id)
        if n_ricette:
            raise ConflittoError(
                f"Non puoi eliminare «{ing.nome}»: compare in {_conta(n_ricette, 'ricetta', 'ricette')}. "
                "Toglilo prima da quelle ricette."
            )
        try:
            self._ingredienti.delete(ingrediente_id)
        except mysql.connector.IntegrityError:
            # qualcuno l'ha aggiunto a una ricetta proprio ora
            raise ConflittoError(f"Non puoi eliminare «{ing.nome}»: è appena stato usato in una ricetta.")
        return ing.nome

    def _carica_ingrediente(self, ingrediente_id):
        ing = self._ingredienti.find_by_id(ingrediente_id)
        if ing is None:
            raise RisorsaNonTrovataError("Ingrediente non trovato.")
        return ing

    # ---------- ricette ----------
    def ricette(self, admin, q, solo_senza_autore, pagina):
        self._solo_admin(admin)
        q = (q or "").strip()[:100]
        totale = self._ricette.conta_admin(q, solo_senza_autore)
        pagine = max(1, ceil(totale / RICETTE_PER_PAGINA))
        pagina = min(max(pagina or 1, 1), pagine)
        items = self._ricette.cerca_admin(q, solo_senza_autore, RICETTE_PER_PAGINA,
                                          (pagina - 1) * RICETTE_PER_PAGINA)
        return PaginaDTO([RicettaAdminDTO.from_model(r) for r in items], pagina, pagine, totale)

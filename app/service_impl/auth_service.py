import mysql.connector
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app.dto.auth_dto import AggiornaProfiloDTO, LoginDTO, RegistrazioneDTO, UtenteDTO
from app.exceptions import (
    ConflittoError,
    CredenzialiNonValideError,
    RisorsaNonTrovataError,
)
from app.models.utente import Utente
from app.repositories.utente_repository import UtenteRepository
from app.service_interface.auth_service_interface import AuthServiceInterface

_ph = PasswordHasher()                       # Argon2id
_HASH_FINTO = _ph.hash("password-finta-per-equalizzare-i-tempi")


class AuthService(AuthServiceInterface):
    """Regole di business e validazioni."""

    def __init__(self, repository: UtenteRepository):
        self._repo = repository

    # ---- registrazione ----
    def registra(self, dto: RegistrazioneDTO) -> UtenteDTO:
        if self._repo.exists_by_username(dto.username) or self._repo.exists_by_email(dto.email):
            raise ConflittoError("Username o email già in uso.")

        utente = Utente(
            username=dto.username,
            email=dto.email,
            password_hash=_ph.hash(dto.password),
        )
        try:
            utente.id = self._repo.save(utente)
        except mysql.connector.IntegrityError:
            # doppia registrazione simultanea: ha vinto l'altra richiesta
            raise ConflittoError("Username o email già in uso.")
        return UtenteDTO.from_model(utente)

    # ---- login ----
    def login(self, dto: LoginDTO) -> UtenteDTO:
        utente = self._repo.find_by_identificativo(dto.identificativo) if dto.identificativo else None
        hash_da_verificare = utente.password_hash if utente else _HASH_FINTO
        try:
            _ph.verify(hash_da_verificare, dto.password)
            valida = utente is not None
        except (VerificationError, InvalidHashError):
            valida = False
        if not valida:
            # stesso messaggio per "utente inesistente" e "password errata"
            raise CredenzialiNonValideError("Username/email o password non corretti.")
        return UtenteDTO.from_model(utente)

    # ---- lettura ----
    def get_utente(self, utente_id: int) -> UtenteDTO:
        utente = self._repo.find_by_id(utente_id)
        if utente is None:
            raise RisorsaNonTrovataError("Utente non trovato.")
        return UtenteDTO.from_model(utente)

    def aggiorna_profilo(self, utente_id: int, dto: AggiornaProfiloDTO) -> UtenteDTO:
        # Verifica se username o email appartengono già a un altro utente
        esistente_u = self._repo.find_by_identificativo(dto.username)
        if esistente_u and esistente_u.id != utente_id:
            raise ConflittoError("Username già in uso.")
        
        esistente_e = self._repo.find_by_identificativo(dto.email)
        if esistente_e and esistente_e.id != utente_id:
            raise ConflittoError("Email già in uso.")

        self._repo.update_profilo(utente_id, dto.username, dto.email)
        utente_aggiornato = self._repo.find_by_id(utente_id)
        return UtenteDTO.from_model(utente_aggiornato)
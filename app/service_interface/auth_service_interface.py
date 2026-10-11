from abc import ABC, abstractmethod

from app.dto.auth_dto import AggiornaProfiloDTO, LoginDTO, RegistrazioneDTO, UtenteDTO


class AuthServiceInterface(ABC):
    """Contratto del servizio di autenticazione."""

    @abstractmethod
    def registra(self, dto: RegistrazioneDTO) -> UtenteDTO: ...

    @abstractmethod
    def login(self, dto: LoginDTO) -> UtenteDTO: ...

    @abstractmethod
    def get_utente(self, utente_id: int) -> UtenteDTO: ...

    @abstractmethod
    def aggiorna_profilo(self, utente_id: int, dto: AggiornaProfiloDTO) -> UtenteDTO: ...
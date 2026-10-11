"""Wiring delle dipendenze (l'iniezione, a mano)."""
from app.repositories.dispensa_repository import DispensaRepository
from app.repositories.ingrediente_repository import IngredienteRepository
from app.repositories.ricetta_repository import RicettaRepository
from app.repositories.utente_repository import UtenteRepository
from app.service_impl.auth_service import AuthService
from app.service_impl.dispensa_service import DispensaService
from app.service_impl.ingrediente_service import IngredienteService
from app.service_impl.ricetta_service import RicettaService
from app.service_interface.auth_service_interface import AuthServiceInterface
from app.service_interface.dispensa_service_interface import DispensaServiceInterface
from app.service_interface.ingrediente_service_interface import IngredienteServiceInterface
from app.service_interface.ricetta_service_interface import RicettaServiceInterface

utente_repository = UtenteRepository()
ricetta_repository = RicettaRepository()
ingrediente_repository = IngredienteRepository()
dispensa_repository = DispensaRepository()

auth_service: AuthServiceInterface = AuthService(utente_repository)
ingrediente_service: IngredienteServiceInterface = IngredienteService(ingrediente_repository)
ricetta_service: RicettaServiceInterface = RicettaService(
    ricetta_repository, ingrediente_repository, dispensa_repository)
dispensa_service: DispensaServiceInterface = DispensaService(
    dispensa_repository, ingrediente_repository, ricetta_service)

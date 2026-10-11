from types import SimpleNamespace

import pytest

import app as app_pkg
import app.controllers.auth_controller as ctrl_auth
import app.controllers.dispensa_controller as ctrl_dispensa
import app.controllers.ingredienti_controller as ctrl_ingredienti
import app.controllers.ricette_controller as ctrl_ricette
from app import create_app
from app.service_impl.auth_service import AuthService
from app.service_impl.dispensa_service import DispensaService
from app.service_impl.ingrediente_service import IngredienteService
from app.service_impl.ricetta_service import RicettaService
from tests.fakes import (
    FakeDispensaRepository, FakeIngredienteRepository, FakeRicettaRepository, FakeUtenteRepository,
)

PASSWORD = "Password123x"


@pytest.fixture
def repo():
    utenti = FakeUtenteRepository()
    ingredienti = FakeIngredienteRepository()
    ricette = FakeRicettaRepository(ingredienti)
    dispensa = FakeDispensaRepository(ingredienti, ricette)
    return SimpleNamespace(utenti=utenti, ingredienti=ingredienti, ricette=ricette, dispensa=dispensa)


@pytest.fixture
def servizi(repo):
    ricetta = RicettaService(repo.ricette, repo.ingredienti, repo.dispensa)
    return SimpleNamespace(
        auth=AuthService(repo.utenti),
        ingrediente=IngredienteService(repo.ingredienti),
        ricetta=ricetta,
        dispensa=DispensaService(repo.dispensa, repo.ingredienti, ricetta),
    )


@pytest.fixture
def flask_app(servizi, monkeypatch):
    """App Flask vera, ma con i service collegati ai repository finti."""
    monkeypatch.setattr(app_pkg, "auth_service", servizi.auth)
    monkeypatch.setattr(ctrl_auth, "auth_service", servizi.auth)
    monkeypatch.setattr(ctrl_ricette, "ricetta_service", servizi.ricetta)
    monkeypatch.setattr(ctrl_dispensa, "ricetta_service", servizi.ricetta)
    monkeypatch.setattr(ctrl_dispensa, "dispensa_service", servizi.dispensa)
    monkeypatch.setattr(ctrl_ingredienti, "ingrediente_service", servizi.ingrediente)
    return create_app({"SECRET_KEY": "test", "WTF_CSRF_ENABLED": False, "RATELIMIT_ENABLED": False,
                        "LOG_TO_FILE": False})


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()


def registra(client, username, email):
    return client.post("/auth/registrati", data={
        "username": username, "email": email, "password": PASSWORD, "conferma_password": PASSWORD})


def accedi(client, username):
    return client.post("/auth/login", data={"identificativo": username, "password": PASSWORD})


@pytest.fixture
def client_loggato(client):
    registra(client, "madalina", "madalina@domain.it")
    accedi(client, "madalina")
    return client


@pytest.fixture
def ingredienti_base(repo):
    """Spaghetti(1) Uova(2) Guanciale(3)."""
    for nome, unita in [("Spaghetti", "g"), ("Uova", "pz"), ("Guanciale", "g")]:
        repo.ingredienti.save(nome, unita)
    return repo.ingredienti

from decimal import Decimal

import pytest

from app.dto.auth_dto import LoginDTO, RegistrazioneDTO
from app.dto.dispensa_dto import DispensaFormDTO
from app.dto.ricetta_dto import RicettaFormDTO
from app.dto.validazione import valida
from app.exceptions import ValidazioneError

REG = dict(username="madalina_1", email="Madalina@Domain.IT",
           password="Password123x", conferma_password="Password123x")

RICETTA = dict(titolo="Carbonara", descrizione="", istruzioni="Rosola il guanciale e mescola.",
               porzioni="4", minuti="25", difficolta="media",
               righe=[{"ingrediente_id": "1", "quantita": "320"}])


def errori_di(modello, base, **modifiche):
    with pytest.raises(ValidazioneError) as e:
        valida(modello, {**base, **modifiche})
    return e.value.errori


# ---------- registrazione ----------
def test_registrazione_valida_e_normalizza_email():
    dto = valida(RegistrazioneDTO, {**REG, "username": "  madalina_1  "})
    assert dto.email == "madalina@domain.it"
    assert dto.username == "madalina_1"


def test_password_non_viene_ripulita_dagli_spazi():
    dto = valida(RegistrazioneDTO, {**REG, "password": " Password123x ", "conferma_password": " Password123x "})
    assert dto.password == " Password123x "


@pytest.mark.parametrize("modifiche, campo", [
    ({"username": "ab"}, "username"),
    ({"username": "nome con spazi"}, "username"),
    ({"email": "non-una-email"}, "email"),
    ({"password": "corta1", "conferma_password": "corta1"}, "password"),
    ({"password": "SoloLettereLunghe", "conferma_password": "SoloLettereLunghe"}, "password"),
    ({"password": "madalina_1", "conferma_password": "madalina_1"}, "password"),
    ({"conferma_password": "Diversa123x"}, "conferma_password"),
])
def test_registrazione_non_valida(modifiche, campo):
    assert campo in errori_di(RegistrazioneDTO, REG, **modifiche)


def test_messaggi_in_italiano():
    errori = errori_di(RegistrazioneDTO, REG, username="ab", conferma_password="x")
    assert errori["username"] == "Almeno 3 caratteri."
    assert errori["conferma_password"] == "Le due password non coincidono."


def test_campo_mancante():
    assert errori_di(LoginDTO, {"identificativo": "a"}, )["password"] == "Campo obbligatorio."


# ---------- ricetta ----------
def test_ricetta_valida_con_virgola_decimale():
    dto = valida(RicettaFormDTO, {**RICETTA, "righe": [{"ingrediente_id": "1", "quantita": "150,5"}]})
    assert dto.righe[0].quantita == Decimal("150.5")
    assert dto.porzioni == 4


@pytest.mark.parametrize("modifiche, campo, parte_messaggio", [
    ({"titolo": "x"}, "titolo", "Almeno 3"),
    ({"porzioni": "abc"}, "porzioni", "numero intero"),
    ({"porzioni": "0"}, "porzioni", "minimo"),
    ({"minuti": "5000"}, "minuti", "massimo"),
    ({"difficolta": "impossibile"}, "difficolta", "valido"),
    ({"righe": []}, "ingredienti", "almeno un ingrediente"),
    ({"righe": [{"ingrediente_id": "1", "quantita": "-5"}]}, "ingredienti", "quantità maggiore di 0"),
    ({"righe": [{"ingrediente_id": "", "quantita": "5"}]}, "ingredienti", "ha bisogno"),
    ({"righe": [{"ingrediente_id": "1", "quantita": "abc"}]}, "ingredienti", "ha bisogno"),
    ({"righe": [{"ingrediente_id": "1", "quantita": "1"}, {"ingrediente_id": "1", "quantita": "2"}]},
     "ingredienti", "ripetuto"),
])
def test_ricetta_non_valida(modifiche, campo, parte_messaggio):
    errori = errori_di(RicettaFormDTO, RICETTA, **modifiche)
    assert parte_messaggio in errori[campo]


# ---------- dispensa ----------
def test_dispensa_quantita_con_virgola():
    assert valida(DispensaFormDTO, {"ingrediente_id": "2", "quantita": "2,5"}).quantita == Decimal("2.5")


@pytest.mark.parametrize("quantita", ["0", "-1", "abc", "1e400", "NaN", "2000000", "1.234"])
def test_dispensa_quantita_non_valida(quantita):
    assert "quantita" in errori_di(DispensaFormDTO, {"ingrediente_id": "1"}, quantita=quantita)

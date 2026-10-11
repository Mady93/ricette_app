import pytest

from app.dto.auth_dto import LoginDTO, RegistrazioneDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, CredenzialiNonValideError, RisorsaNonTrovataError

REG = dict(username="madalina", email="m@domain.it", password="Password123x", conferma_password="Password123x")


def registra(servizi, **modifiche):
    return servizi.auth.registra(valida(RegistrazioneDTO, {**REG, **modifiche}))


def test_la_password_viene_salvata_come_hash_argon2(servizi, repo):
    utente = registra(servizi)
    salvato = repo.utenti.d[utente.id]
    assert salvato.password_hash.startswith("$argon2id$")
    assert "Password123x" not in salvato.password_hash


def test_il_dto_di_ritorno_non_espone_l_hash(servizi):
    assert not hasattr(registra(servizi), "password_hash")


def test_username_o_email_gia_usati(servizi):
    registra(servizi)
    with pytest.raises(ConflittoError):
        registra(servizi, email="altra@domain.it")          # stesso username
    with pytest.raises(ConflittoError):
        registra(servizi, username="altro")                 # stessa email


def test_login_con_username_e_con_email(servizi):
    registra(servizi)
    for ident in ("madalina", "m@domain.it", "M@Domain.it"):
        assert servizi.auth.login(LoginDTO(identificativo=ident, password="Password123x")).username == "madalina"


def test_login_fallito_ha_sempre_lo_stesso_messaggio(servizi):
    registra(servizi)
    with pytest.raises(CredenzialiNonValideError) as sbagliata:
        servizi.auth.login(LoginDTO(identificativo="madalina", password="Sbagliata123"))
    with pytest.raises(CredenzialiNonValideError) as inesistente:
        servizi.auth.login(LoginDTO(identificativo="nessuno", password="Password123x"))
    assert sbagliata.value.message == inesistente.value.message


def test_utente_inesistente(servizi):
    with pytest.raises(RisorsaNonTrovataError):
        servizi.auth.get_utente(999)

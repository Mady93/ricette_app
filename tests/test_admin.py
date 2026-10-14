"""Area admin: regole del service (con repository finti) e comportamento delle rotte HTTP."""
import pytest

from app.dto.admin_dto import CambioRuoloDTO
from app.dto.auth_dto import RegistrazioneDTO
from app.dto.dispensa_dto import DispensaFormDTO
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.ricetta_dto import RicettaFormDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, NonAutorizzatoError, RisorsaNonTrovataError, ValidazioneError

PASSWORD = "Password123x"


# ---------------- helper ----------------
def crea_utente(servizi, repo, username, ruolo="utente"):
    u = servizi.auth.registra(valida(RegistrazioneDTO, {
        "username": username, "email": f"{username}@domain.it",
        "password": PASSWORD, "conferma_password": PASSWORD}))
    repo.utenti.d[u.id].ruolo = ruolo
    return servizi.auth.get_utente(u.id)          # DTO "fresco", con il ruolo aggiornato


def crea_ricetta(servizi, autore_id, titolo="Pasta semplice", righe=((1, 100),)):
    return servizi.ricetta.crea(autore_id, valida(RicettaFormDTO, {
        "titolo": titolo, "descrizione": "", "istruzioni": "Cuoci la pasta e condiscila.",
        "porzioni": "4", "minuti": "20", "difficolta": "facile",
        "righe": [{"ingrediente_id": str(i), "quantita": str(q)} for i, q in righe]}))


def in_dispensa(servizi, utente_id, ingrediente_id, quantita="100"):
    servizi.dispensa.imposta(utente_id, valida(DispensaFormDTO, {
        "ingrediente_id": str(ingrediente_id), "quantita": quantita}))


@pytest.fixture
def admin(servizi, repo):
    return crea_utente(servizi, repo, "capo", "admin")


@pytest.fixture
def mario(servizi, repo):
    return crea_utente(servizi, repo, "mario")


# =============== SERVICE: permessi ===============
CHIAMATE = [
    lambda s, u: s.admin.statistiche(u),
    lambda s, u: s.admin.utenti(u),
    lambda s, u: s.admin.cambia_ruolo(u, 99, CambioRuoloDTO(ruolo="admin")),
    lambda s, u: s.admin.elimina_utente(u, 99),
    lambda s, u: s.admin.ingredienti(u),
    lambda s, u: s.admin.ingrediente(u, 99),
    lambda s, u: s.admin.modifica_ingrediente(u, 99, IngredienteFormDTO(nome="Sale", unita="g")),
    lambda s, u: s.admin.elimina_ingrediente(u, 99),
    lambda s, u: s.admin.ricette(u, "", False, 1),
]


@pytest.mark.parametrize("chiamata", CHIAMATE)
def test_ogni_operazione_admin_rifiuta_un_utente_normale(servizi, mario, chiamata):
    # l'id 99 non esiste: il controllo dei permessi deve scattare PRIMA di cercare la risorsa
    with pytest.raises(NonAutorizzatoError):
        chiamata(servizi, mario)


# =============== SERVICE: utenti ===============
def test_admin_promuove_e_declassa(servizi, repo, admin, mario):
    servizi.admin.cambia_ruolo(admin, mario.id, CambioRuoloDTO(ruolo="admin"))
    assert repo.utenti.d[mario.id].ruolo == "admin"
    servizi.admin.cambia_ruolo(admin, mario.id, CambioRuoloDTO(ruolo="utente"))
    assert repo.utenti.d[mario.id].ruolo == "utente"


def test_non_puoi_cambiare_il_tuo_ruolo_ne_eliminarti(servizi, repo, admin):
    with pytest.raises(ConflittoError):
        servizi.admin.cambia_ruolo(admin, admin.id, CambioRuoloDTO(ruolo="utente"))
    with pytest.raises(ConflittoError):
        servizi.admin.elimina_utente(admin, admin.id)
    assert repo.utenti.d[admin.id].ruolo == "admin"          # resta sempre almeno un admin


def test_ruolo_inventato_viene_rifiutato_dal_dto():
    with pytest.raises(ValidazioneError):
        valida(CambioRuoloDTO, {"ruolo": "superuser"})


def test_utente_inesistente(servizi, admin):
    with pytest.raises(RisorsaNonTrovataError):
        servizi.admin.cambia_ruolo(admin, 999, CambioRuoloDTO(ruolo="admin"))
    with pytest.raises(RisorsaNonTrovataError):
        servizi.admin.elimina_utente(admin, 999)


def test_eliminare_un_utente_lascia_le_ricette_senza_autore(servizi, repo, admin, mario, ingredienti_base):
    rid = crea_ricetta(servizi, mario.id)
    servizi.admin.elimina_utente(admin, mario.id)
    assert mario.id not in repo.utenti.d
    assert repo.ricette.d[rid].utente_id is None


def test_lista_utenti_con_numero_di_ricette(servizi, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, "Ricetta uno")
    crea_ricetta(servizi, mario.id, "Ricetta due")
    righe = {u.username: u.n_ricette for u in servizi.admin.utenti(admin)}
    assert righe == {"capo": 0, "mario": 2}


# =============== SERVICE: ingredienti ===============
def test_rinomina_ingrediente(servizi, repo, admin, ingredienti_base):
    servizi.admin.modifica_ingrediente(admin, 1, IngredienteFormDTO(nome="Spaghettoni", unita="g"))
    assert repo.ingredienti.d[1].nome == "Spaghettoni"


def test_rinomina_con_nome_gia_usato_da_un_altro(servizi, admin, ingredienti_base):
    with pytest.raises(ConflittoError):
        servizi.admin.modifica_ingrediente(admin, 1, IngredienteFormDTO(nome="Uova", unita="g"))


def test_si_puo_salvare_senza_cambiare_il_nome(servizi, admin, ingredienti_base):
    # nome invariato: non e' un conflitto con "se stesso"
    servizi.admin.modifica_ingrediente(admin, 1, IngredienteFormDTO(nome="Spaghetti", unita="g"))


def test_unita_bloccata_se_usato_in_una_ricetta(servizi, repo, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, righe=((1, 100),))
    with pytest.raises(ConflittoError):
        servizi.admin.modifica_ingrediente(admin, 1, IngredienteFormDTO(nome="Spaghetti", unita="pz"))
    assert repo.ingredienti.d[1].unita_base == "g"


def test_unita_bloccata_se_presente_in_una_dispensa(servizi, admin, mario, ingredienti_base):
    in_dispensa(servizi, mario.id, 2)
    with pytest.raises(ConflittoError):
        servizi.admin.modifica_ingrediente(admin, 2, IngredienteFormDTO(nome="Uova", unita="g"))


def test_unita_modificabile_se_non_usato(servizi, repo, admin, ingredienti_base):
    servizi.admin.modifica_ingrediente(admin, 3, IngredienteFormDTO(nome="Guanciale", unita="pz"))
    assert repo.ingredienti.d[3].unita_base == "pz"


def test_ingrediente_usato_in_ricetta_non_si_elimina(servizi, repo, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, righe=((1, 100),))
    with pytest.raises(ConflittoError):
        servizi.admin.elimina_ingrediente(admin, 1)
    assert 1 in repo.ingredienti.d


def test_ingrediente_solo_in_dispensa_si_elimina_e_sparisce_dalla_dispensa(servizi, repo, admin, mario, ingredienti_base):
    in_dispensa(servizi, mario.id, 3)
    assert servizi.admin.elimina_ingrediente(admin, 3) == "Guanciale"
    assert 3 not in repo.ingredienti.d
    assert (mario.id, 3) not in repo.dispensa.d


def test_ingrediente_inesistente(servizi, admin):
    with pytest.raises(RisorsaNonTrovataError):
        servizi.admin.elimina_ingrediente(admin, 999)
    with pytest.raises(RisorsaNonTrovataError):
        servizi.admin.ingrediente(admin, 999)


def test_elenco_ingredienti_con_utilizzi(servizi, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, righe=((1, 100), (2, 4)))
    in_dispensa(servizi, mario.id, 1)
    righe = {i.nome: (i.n_ricette, i.n_dispense, i.eliminabile) for i in servizi.admin.ingredienti(admin)}
    assert righe == {"Spaghetti": (1, 1, False), "Uova": (1, 0, False), "Guanciale": (0, 0, True)}


# =============== SERVICE: ricette e statistiche ===============
def test_lista_ricette_admin_paginata_e_con_autore(servizi, admin, mario, ingredienti_base):
    for n in range(25):
        crea_ricetta(servizi, mario.id, f"Ricetta {n:02d}")
    prima = servizi.admin.ricette(admin, "", False, 1)
    assert (prima.totale, prima.pagine, len(prima.items)) == (25, 2, 20)
    assert prima.items[0].autore == "mario"
    assert len(servizi.admin.ricette(admin, "", False, 2).items) == 5
    assert servizi.admin.ricette(admin, "", False, 99).pagina == 2        # pagina fuori intervallo -> ultima


def test_filtri_lista_ricette_admin(servizi, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, "Carbonara")
    crea_ricetta(servizi, mario.id, "Frittata")
    assert [r.titolo for r in servizi.admin.ricette(admin, "carbo", False, 1).items] == ["Carbonara"]
    servizi.admin.elimina_utente(admin, mario.id)                        # le ricette restano senza autore
    senza = servizi.admin.ricette(admin, "", True, 1)
    assert senza.totale == 2 and all(r.autore is None for r in senza.items)


def test_statistiche(servizi, admin, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, righe=((1, 100),))
    s = servizi.admin.statistiche(admin)
    assert (s.utenti, s.amministratori) == (2, 1)
    assert (s.ricette, s.ricette_senza_autore) == (1, 0)
    assert (s.ingredienti, s.ingredienti_inutilizzati) == (3, 2)


# =============== HTTP: accesso e menu ===============
PAGINE_ADMIN = ["/admin", "/admin/utenti", "/admin/ingredienti", "/admin/ricette"]


def test_ospite_viene_mandato_al_login(client):
    r = client.get("/admin")
    assert r.status_code == 302 and "/auth/login" in r.headers["Location"]


@pytest.mark.parametrize("percorso", PAGINE_ADMIN + ["/admin/ingredienti/1/modifica"])
def test_utente_normale_non_entra_nelle_pagine_admin(client_loggato, percorso):
    assert client_loggato.get(percorso).status_code == 403


@pytest.mark.parametrize("percorso", [
    "/admin/utenti/1/ruolo", "/admin/utenti/1/elimina",
    "/admin/ingredienti/1/elimina", "/admin/ricette/1/elimina"])
def test_utente_normale_non_puo_eseguire_azioni_admin(client_loggato, percorso):
    assert client_loggato.post(percorso, data={"ruolo": "admin"}).status_code == 403


def test_admin_apre_tutte_le_pagine(client_admin, ingredienti_base):
    for percorso in PAGINE_ADMIN + ["/admin/ingredienti/1/modifica"]:
        assert client_admin.get(percorso).status_code == 200, percorso


def test_il_dropdown_admin_compare_per_gli_admin(client_admin):
    pagina = client_admin.get("/").data
    assert b"menuAdmin" in pagina
    for voce in (b"/admin/utenti", b"/admin/ingredienti", b"/admin/ricette",
                 b"/ingredienti/importa", b"/ricette/importa"):
        assert voce in pagina


def test_ospite_non_vede_il_dropdown(client):
    assert b"menuAdmin" not in client.get("/").data


def test_utente_normale_non_vede_il_dropdown_ma_vede_la_dispensa(client_loggato):
    pagina = client_loggato.get("/").data
    assert b"menuAdmin" not in pagina and b"/admin" not in pagina
    assert b"/dispensa" in pagina


# =============== HTTP: azioni ===============
def test_admin_cambia_ruolo_da_http(client_admin, servizi, repo, mario):
    r = client_admin.post(f"/admin/utenti/{mario.id}/ruolo", data={"ruolo": "admin"}, follow_redirects=True)
    assert r.status_code == 200 and repo.utenti.d[mario.id].ruolo == "admin"
    assert "ora ha il ruolo admin".encode() in r.data


def test_admin_non_puo_declassare_se_stesso_da_http(client_admin, repo):
    r = client_admin.post("/admin/utenti/1/ruolo", data={"ruolo": "utente"}, follow_redirects=True)
    assert repo.utenti.d[1].ruolo == "admin"
    assert b"Non puoi cambiare il tuo stesso ruolo" in r.data


def test_ruolo_non_valido_da_http(client_admin, repo, mario):
    r = client_admin.post(f"/admin/utenti/{mario.id}/ruolo", data={"ruolo": "dio"}, follow_redirects=True)
    assert repo.utenti.d[mario.id].ruolo == "utente" and b"Ruolo non valido" in r.data


def test_admin_elimina_ricetta_e_torna_alla_lista(client_admin, servizi, repo, mario, ingredienti_base):
    rid = crea_ricetta(servizi, mario.id)
    r = client_admin.post(f"/admin/ricette/{rid}/elimina", data={"pagina": "1"})
    assert r.status_code == 302 and "/admin/ricette" in r.headers["Location"]
    assert rid not in repo.ricette.d


def test_rinomina_ingrediente_in_conflitto_mostra_l_errore(client_admin, ingredienti_base):
    r = client_admin.post("/admin/ingredienti/1/modifica", data={"nome": "Uova", "unita": "g"})
    assert r.status_code == 409 and b"Esiste gi" in r.data


def test_admin_modifica_ingrediente_da_http(client_admin, repo, ingredienti_base):
    r = client_admin.post("/admin/ingredienti/3/modifica", data={"nome": "Pancetta", "unita": "g"})
    assert r.status_code == 302 and repo.ingredienti.d[3].nome == "Pancetta"


def test_elimina_ingrediente_usato_viene_rifiutato_da_http(client_admin, servizi, repo, mario, ingredienti_base):
    crea_ricetta(servizi, mario.id, righe=((1, 100),))
    r = client_admin.post("/admin/ingredienti/1/elimina", follow_redirects=True)
    assert 1 in repo.ingredienti.d and b"compare in 1 ricetta" in r.data

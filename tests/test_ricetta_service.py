import pytest

from app.dto.auth_dto import UtenteDTO
from app.dto.dispensa_dto import DispensaFormDTO
from app.dto.ricetta_dto import RicettaFormDTO
from app.dto.validazione import valida
from app.exceptions import NonAutorizzatoError, RisorsaNonTrovataError, ValidazioneError

BASE = dict(titolo="Carbonara", descrizione="", istruzioni="Rosola il guanciale e mescola.",
            porzioni="4", minuti="25", difficolta="media")


def dto_ricetta(righe, **modifiche):
    return valida(RicettaFormDTO, {**BASE, **modifiche, "righe": [
        {"ingrediente_id": str(i), "quantita": str(q)} for i, q in righe]})


def utente(id=1, ruolo="utente"):
    return UtenteDTO(id=id, username=f"u{id}", email=f"u{id}@domain.it", ruolo=ruolo)


def test_ingrediente_inesistente_viene_rifiutato(servizi, ingredienti_base):
    with pytest.raises(ValidazioneError) as e:
        servizi.ricetta.crea(1, dto_ricetta([(99, 100)]))
    assert "ingredienti" in e.value.errori


def test_dettaglio_scala_le_quantita_con_le_porzioni(servizi, ingredienti_base):
    rid = servizi.ricetta.crea(1, dto_ricetta([(1, 320), (2, 4)]))
    det = servizi.ricetta.dettaglio(rid, 8, None)
    quantita = {r.nome: r.quantita for r in det.righe}
    assert quantita == {"Spaghetti": 640.0, "Uova": 8.0}
    assert det.porzioni == 8 and det.porzioni_base == 4


def test_porzioni_fuori_limite_tornano_alla_base(servizi, ingredienti_base):
    rid = servizi.ricetta.crea(1, dto_ricetta([(1, 320)]))
    assert servizi.ricetta.dettaglio(rid, 9999, None).porzioni == 4


def test_ricetta_inesistente(servizi):
    with pytest.raises(RisorsaNonTrovataError):
        servizi.ricetta.dettaglio(42, None, None)


def test_solo_l_autore_o_un_admin_modifica_ed_elimina(servizi, ingredienti_base):
    rid = servizi.ricetta.crea(1, dto_ricetta([(1, 320)]))
    nuovo = dto_ricetta([(1, 300)], titolo="Carbonara vera")
    with pytest.raises(NonAutorizzatoError):
        servizi.ricetta.modifica(utente(id=2), rid, nuovo)
    with pytest.raises(NonAutorizzatoError):
        servizi.ricetta.elimina(utente(id=2), rid)
    servizi.ricetta.modifica(utente(id=1), rid, nuovo)                  # l'autore
    servizi.ricetta.modifica(utente(id=3, ruolo="admin"), rid, nuovo)   # un admin
    servizi.ricetta.elimina(utente(id=1), rid)
    with pytest.raises(RisorsaNonTrovataError):
        servizi.ricetta.dettaglio(rid, None, None)


def test_paginazione_e_pagina_fuori_intervallo(servizi, ingredienti_base):
    for n in range(12):
        servizi.ricetta.crea(1, dto_ricetta([(1, 100)], titolo=f"Ricetta {n:02d}"))
    prima = servizi.ricetta.elenco("", None, None, 1)
    assert (prima.totale, prima.pagine, len(prima.items)) == (12, 2, 9)
    assert servizi.ricetta.elenco("", None, None, 99).pagina == 2        # pagina 99 -> ultima
    assert servizi.ricetta.elenco("", None, None, -5).pagina == 1


def test_filtri_con_valori_strani_vengono_ignorati(servizi, ingredienti_base):
    servizi.ricetta.crea(1, dto_ricetta([(1, 100)]))
    assert servizi.ricetta.elenco("", "inventata", 99999, 1).totale == 1


def test_lista_spesa_contiene_solo_quello_che_manca(servizi, ingredienti_base):
    rid = servizi.ricetta.crea(1, dto_ricetta([(1, 320), (2, 4), (3, 150)]))
    servizi.dispensa.imposta(7, valida(DispensaFormDTO, {"ingrediente_id": "1", "quantita": "500"}))
    servizi.dispensa.imposta(7, valida(DispensaFormDTO, {"ingrediente_id": "2", "quantita": "1"}))
    spesa = {v.nome: v.quantita for v in servizi.dispensa.lista_spesa(7, rid, 4)}
    assert spesa == {"Uova": 3.0, "Guanciale": 150.0}                   # spaghetti: ne ha abbastanza


def test_suggerimenti_ordinati_per_percentuale(servizi, ingredienti_base):
    completa = servizi.ricetta.crea(1, dto_ricetta([(1, 100)], titolo="Solo pasta"))
    servizi.ricetta.crea(1, dto_ricetta([(1, 100), (2, 4), (3, 50)], titolo="Carbonara"))
    servizi.dispensa.imposta(7, valida(DispensaFormDTO, {"ingrediente_id": "1", "quantita": "500"}))
    sugg = servizi.dispensa.cosa_posso_cucinare(7)
    assert [s.titolo for s in sugg] == ["Solo pasta", "Carbonara"]
    assert (sugg[0].percentuale, sugg[1].percentuale) == (100, 33)


def test_dispensa_rifiuta_ingrediente_inesistente(servizi, ingredienti_base):
    with pytest.raises(ValidazioneError):
        servizi.dispensa.imposta(7, valida(DispensaFormDTO, {"ingrediente_id": "99", "quantita": "5"}))

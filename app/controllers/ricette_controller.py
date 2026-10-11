import logging

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.container import ricetta_service
from app.dto.ricetta_dto import RicettaFormDati, RicettaFormDTO
from app.dto.validazione import valida
from app.exceptions import ValidazioneError
from app.utils.decorators import login_required

log = logging.getLogger(__name__)
ricette_bp = Blueprint("ricette", __name__, url_prefix="/ricette")


@ricette_bp.route("")
def elenco():
    q = request.args.get("q", "")
    difficolta = request.args.get("difficolta", "")
    max_minuti = request.args.get("max_minuti", type=int)
    pagina = request.args.get("pagina", 1, type=int)
    
    # Legge il valore scelto dall'utente (default 5) e valida che sia tra i numeri primi consentiti
    per_page = request.args.get("per_page", 5, type=int)
    if per_page not in [5, 11, 23, 47, 97]:
        per_page = 5

    # Passa il per_page al servizio
    pag = ricetta_service.elenco(q, difficolta or None, max_minuti, pagina, per_page)
    
    # Passa il per_page al template HTML per mantenere la select selezionata
    return render_template(
        "ricette/elenco.html", 
        pag=pag, 
        q=q.strip()[:100],
        difficolta=difficolta, 
        max_minuti=max_minuti or "",
        per_page=per_page
    )


@ricette_bp.route("/<int:ricetta_id>")
def dettaglio(ricetta_id):
    porzioni = request.args.get("porzioni", type=int)
    utente_id = g.utente.id if g.utente else None
    r = ricetta_service.dettaglio(ricetta_id, porzioni, utente_id)
    return render_template("ricette/dettaglio.html", r=r)


def _form(dto, errori, azione, titolo_pagina, status=200):
    return render_template(
        "ricette/form.html", dto=dto, errori=errori, azione=azione, titolo_pagina=titolo_pagina,
        ingredienti=ricetta_service.ingredienti_disponibili(),
    ), status


@ricette_bp.route("/nuova", methods=["GET", "POST"])
@login_required
def nuova():
    azione = url_for("ricette.nuova")
    if request.method == "POST":
        dati = RicettaFormDati.da_form(request.form)
        try:
            nuovo_id = ricetta_service.crea(g.utente.id, valida(RicettaFormDTO, dati.come_dict()))
        except ValidazioneError as e:
            return _form(dati, e.errori, azione, "Nuova ricetta", 400)
        log.info("ricetta creata", extra={"evento": "ricetta_creata", "ricetta_id": nuovo_id})
        flash("Ricetta creata.", "success")
        return redirect(url_for("ricette.dettaglio", ricetta_id=nuovo_id))
    return _form(RicettaFormDati(), {}, azione, "Nuova ricetta")


@ricette_bp.route("/<int:ricetta_id>/modifica", methods=["GET", "POST"])
@login_required
def modifica(ricetta_id):
    azione = url_for("ricette.modifica", ricetta_id=ricetta_id)
    if request.method == "POST":
        dati = RicettaFormDati.da_form(request.form)
        try:
            ricetta_service.modifica(g.utente, ricetta_id, valida(RicettaFormDTO, dati.come_dict()))
        except ValidazioneError as e:
            return _form(dati, e.errori, azione, "Modifica ricetta", 400)
        log.info("ricetta modificata", extra={"evento": "ricetta_modificata", "ricetta_id": ricetta_id})
        flash("Ricetta aggiornata.", "success")
        return redirect(url_for("ricette.dettaglio", ricetta_id=ricetta_id))
    return _form(ricetta_service.per_modifica(g.utente, ricetta_id), {}, azione, "Modifica ricetta")


@ricette_bp.route("/<int:ricetta_id>/elimina", methods=["POST"])
@login_required
def elimina(ricetta_id):
    ricetta_service.elimina(g.utente, ricetta_id)
    log.info("ricetta eliminata", extra={"evento": "ricetta_eliminata", "ricetta_id": ricetta_id})
    flash("Ricetta eliminata.", "info")
    return redirect(url_for("ricette.elenco"))

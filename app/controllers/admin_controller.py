"""Area amministratore: dashboard, utenti, ingredienti, ricette.

Ogni rotta e' protetta da @admin_required (non loggato -> login, non admin -> 403) e ogni modifica
passa da POST con token CSRF. Le regole (es. "non puoi eliminare te stesso") stanno nel service.
"""
import logging

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.container import admin_service, ricetta_service
from app.dto.admin_dto import CambioRuoloDTO
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, ValidazioneError
from app.utils.decorators import admin_required

log = logging.getLogger(__name__)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------- dashboard ----------
@admin_bp.route("")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html", s=admin_service.statistiche(g.utente))


# ---------- utenti ----------
@admin_bp.route("/utenti")
@admin_required
def utenti():
    return render_template("admin/utenti.html", utenti=admin_service.utenti(g.utente))


@admin_bp.route("/utenti/<int:utente_id>/ruolo", methods=["POST"])
@admin_required
def cambia_ruolo(utente_id):
    try:
        dto = valida(CambioRuoloDTO, {"ruolo": request.form.get("ruolo", "")})
        u = admin_service.cambia_ruolo(g.utente, utente_id, dto)
    except ValidazioneError:
        flash("Ruolo non valido.", "danger")
    except ConflittoError as e:
        flash(e.message, "danger")
    else:
        log.info("ruolo cambiato", extra={"evento": "admin_ruolo_cambiato",
                                          "utente_target_id": utente_id, "ruolo": u.ruolo})
        flash(f"«{u.username}» ora ha il ruolo {u.ruolo}.", "success")
    return redirect(url_for("admin.utenti"))


@admin_bp.route("/utenti/<int:utente_id>/elimina", methods=["POST"])
@admin_required
def elimina_utente(utente_id):
    try:
        u = admin_service.elimina_utente(g.utente, utente_id)
    except ConflittoError as e:
        flash(e.message, "danger")
    else:
        log.info("utente eliminato", extra={"evento": "admin_utente_eliminato", "utente_target_id": utente_id})
        flash(f"Utente «{u.username}» eliminato. Le sue ricette sono rimaste, senza autore.", "info")
    return redirect(url_for("admin.utenti"))


# ---------- ingredienti ----------
@admin_bp.route("/ingredienti")
@admin_required
def ingredienti():
    return render_template("admin/ingredienti.html", ingredienti=admin_service.ingredienti(g.utente))


@admin_bp.route("/ingredienti/<int:ingrediente_id>/modifica", methods=["GET", "POST"])
@admin_required
def modifica_ingrediente(ingrediente_id):
    ing = admin_service.ingrediente(g.utente, ingrediente_id)
    dati, errori = {"nome": ing.nome, "unita": ing.unita}, {}
    if request.method == "POST":
        dati = {"nome": request.form.get("nome", "").strip(), "unita": request.form.get("unita", "")}
        status = 400
        try:
            admin_service.modifica_ingrediente(g.utente, ingrediente_id, valida(IngredienteFormDTO, dati))
        except ValidazioneError as e:
            errori = e.errori
        except ConflittoError as e:
            errori, status = {"generale": e.message}, 409
        else:
            log.info("ingrediente modificato", extra={"evento": "admin_ingrediente_modificato",
                                                      "ingrediente_id": ingrediente_id})
            flash(f"Ingrediente «{dati['nome']}» aggiornato.", "success")
            return redirect(url_for("admin.ingredienti"))
        return render_template("admin/ingrediente_modifica.html", ing=ing, dati=dati, errori=errori), status
    return render_template("admin/ingrediente_modifica.html", ing=ing, dati=dati, errori=errori)


@admin_bp.route("/ingredienti/<int:ingrediente_id>/elimina", methods=["POST"])
@admin_required
def elimina_ingrediente(ingrediente_id):
    try:
        nome = admin_service.elimina_ingrediente(g.utente, ingrediente_id)
    except ConflittoError as e:
        flash(e.message, "danger")
    else:
        log.info("ingrediente eliminato", extra={"evento": "admin_ingrediente_eliminato",
                                                 "ingrediente_id": ingrediente_id})
        flash(f"Ingrediente «{nome}» eliminato.", "info")
    return redirect(url_for("admin.ingredienti"))


# ---------- ricette ----------
@admin_bp.route("/ricette")
@admin_required
def ricette():
    q = request.args.get("q", "").strip()[:100]
    senza_autore = request.args.get("senza_autore") == "1"
    pagina = request.args.get("pagina", 1, type=int)
    pag = admin_service.ricette(g.utente, q, senza_autore, pagina)
    return render_template("admin/ricette.html", pag=pag, q=q, senza_autore=senza_autore)


@admin_bp.route("/ricette/<int:ricetta_id>/elimina", methods=["POST"])
@admin_required
def elimina_ricetta(ricetta_id):
    ricetta_service.elimina(g.utente, ricetta_id)         # un admin puo' eliminare qualsiasi ricetta
    log.info("ricetta eliminata", extra={"evento": "ricetta_eliminata", "ricetta_id": ricetta_id,
                                         "da_admin": True})
    flash("Ricetta eliminata.", "info")
    # torna alla stessa pagina/filtri da cui arrivi (url_for costruisce un URL interno: niente open redirect)
    return redirect(url_for(
        "admin.ricette",
        pagina=request.form.get("pagina", 1, type=int),
        q=request.form.get("q", "").strip()[:100] or None,
        senza_autore=1 if request.form.get("senza_autore") == "1" else None,
    ))

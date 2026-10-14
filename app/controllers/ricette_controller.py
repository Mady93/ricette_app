import logging

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.container import ricetta_service
from app.dto.ricetta_dto import RicettaFormDati, RicettaFormDTO
from app.dto.validazione import valida
from app.exceptions import ValidazioneError
from app.utils.decorators import login_required, ruolo_richiesto

log = logging.getLogger(__name__)
ricette_bp = Blueprint("ricette", __name__, url_prefix="/ricette")


@ricette_bp.route("")
def elenco():
    """Elenco ricette protetto: se non ci sono ricette, reindirizza alla home."""
    if not ricetta_service.esistono_ricette():
        flash("Il catalogo delle ricette non è ancora disponibile.", "warning")
        return redirect(url_for("main.home"))

    q = request.args.get("q", "")
    difficolta = request.args.get("difficolta", "")
    max_minuti = request.args.get("max_minuti", type=int)
    pagina = request.args.get("pagina", 1, type=int)
    
    per_page = request.args.get("per_page", 5, type=int)
    if per_page not in [5, 11, 23, 47, 97]:
        per_page = 5

    pag = ricetta_service.elenco(q, difficolta or None, max_minuti, pagina, per_page)
    
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
    """Dettaglio ricetta protetto."""
    if not ricetta_service.esistono_ricette():
        return redirect(url_for("main.home"))
        
    porzioni = request.args.get("porzioni", type=int)
    utente_id = g.utente.id if g.utente else None
    r = ricetta_service.dettaglio(ricetta_id, porzioni, utente_id)
    return render_template("ricette/dettaglio.html", r=r)


@ricette_bp.route("/importa", methods=["GET", "POST"])
@ruolo_richiesto("admin")
def importa():
    if request.method == "POST":
        file = request.files.get("file_csv")
        if not file or not file.filename.endswith(".csv"):
            flash("Per favore, carica un file CSV valido.", "danger")
            return redirect(request.url)
            
        try:
            inserite, saltate = ricetta_service.importa_da_csv(file.stream, g.utente.id)
            flash(f"Importazione ricette completata! Aggiunte: {inserite}. Saltate/Errore: {saltate}.", "success")
            return redirect(url_for("ricette.elenco"))
        except Exception as e:
            flash(f"Errore durante l'importazione: {str(e)}", "danger")
            return redirect(request.url)
            
    return render_template("ricette/importa.html")


@ricette_bp.route("/<int:ricetta_id>/modifica", methods=["GET", "POST"])
@ruolo_richiesto("admin")
def modifica(ricetta_id):
    return redirect(url_for("ricette.dettaglio", ricetta_id=ricetta_id))


@ricette_bp.route("/<int:ricetta_id>/elimina", methods=["POST"])
@ruolo_richiesto("admin")
def elimina(ricetta_id):
    ricetta_service.elimina(g.utente, ricetta_id)
    log.info("ricetta eliminata", extra={"evento": "ricetta_eliminata", "ricetta_id": ricetta_id})
    flash("Ricetta eliminata.", "info")
    return redirect(url_for("ricette.elenco"))
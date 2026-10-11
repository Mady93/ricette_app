import csv
import io

from flask import Blueprint, Response, flash, g, redirect, render_template, request, url_for

from app.container import dispensa_service, ricetta_service
from app.dto.dispensa_dto import DispensaFormDTO
from app.dto.validazione import valida
from app.exceptions import ValidazioneError
from app.utils.decorators import login_required
from app.utils.filters import qta

dispensa_bp = Blueprint("dispensa", __name__, url_prefix="/dispensa")


def _pagina(dati: dict, errori: dict, status: int = 200) -> tuple:
    """Renderizza la pagina della dispensa con dati, errori e stato HTTP."""
    return render_template(
        "dispensa/elenco.html", voci=dispensa_service.elenco(g.utente.id),
        ingredienti=ricetta_service.ingredienti_disponibili(), dati=dati, errori=errori,
    ), status


@dispensa_bp.route("")
@login_required
def elenco() -> tuple:
    """Visualizza l'elenco degli ingredienti presenti nella dispensa."""
    return _pagina({"ingrediente_id": "", "quantita": ""}, {})


@dispensa_bp.route("/imposta", methods=["POST"])
@login_required
def imposta() -> tuple:
    """Imposta o aggiorna la quantità di un ingrediente nella dispensa."""
    dati: dict[str, str] = {"ingrediente_id": request.form.get("ingrediente_id", "").strip(),
            "quantita": request.form.get("quantita", "").strip()}
    try:
        dispensa_service.imposta(g.utente.id, valida(DispensaFormDTO, dati))
    except ValidazioneError as e:
        return _pagina(dati, e.errori, 400)
    flash("Dispensa aggiornata.", "success")
    return redirect(url_for("dispensa.elenco"))


@dispensa_bp.route("/<int:ingrediente_id>/rimuovi", methods=["POST"])
@login_required
def rimuovi(ingrediente_id: int) -> tuple:
    """Rimuove un ingrediente dalla dispensa dell'utente."""
    dispensa_service.rimuovi(g.utente.id, ingrediente_id)
    flash("Ingrediente tolto dalla dispensa.", "info")
    return redirect(url_for("dispensa.elenco"))


@dispensa_bp.route("/cosa-cucinare")
@login_required
def cosa_cucinare() -> object:
    """Mostra le ricette cucinabili con gli ingredienti disponibili."""
    return render_template("dispensa/cosa_cucinare.html",
                           suggerimenti=dispensa_service.cosa_posso_cucinare(g.utente.id))


def _cella_sicura(testo: object) -> str:
    """Evita la 'CSV injection': Excel esegue le celle che iniziano con = + - @."""
    testo = str(testo)
    return "'" + testo if testo[:1] in ("=", "+", "-", "@", "\t", "\r") else testo


@dispensa_bp.route("/spesa/<int:ricetta_id>.csv")
@login_required
def spesa_csv(ricetta_id: int) -> Response | tuple:
    """Genera e restituisce la lista della spesa in formato CSV."""
    porzioni = request.args.get("porzioni", type=int)
    voci = dispensa_service.lista_spesa(g.utente.id, ricetta_id, porzioni)
    if not voci:
        flash("Hai già tutti gli ingredienti: niente da comprare!", "info")
        return redirect(url_for("ricette.dettaglio", ricetta_id=ricetta_id))
    buf = io.StringIO()
    scrittore = csv.writer(buf, delimiter=";")                 # separatore per Excel italiano
    scrittore.writerow(["Ingrediente", "Quantità da comprare", "Unità"])
    for v in voci:
        scrittore.writerow([_cella_sicura(v.nome), qta(v.quantita), v.unita])
    risposta = Response("\ufeff" + buf.getvalue(), mimetype="text/csv; charset=utf-8")
    risposta.headers["Content-Disposition"] = f'attachment; filename="lista_spesa_{ricetta_id}.csv"'
    return risposta
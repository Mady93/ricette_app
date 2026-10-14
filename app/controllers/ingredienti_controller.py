from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.container import ingrediente_service, ricetta_service
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, ValidazioneError
from app.utils.decorators import login_required, ruolo_richiesto

ingredienti_bp = Blueprint("ingredienti", __name__, url_prefix="/ingredienti")


@ingredienti_bp.route("/nuovo", methods=["GET", "POST"])
@login_required
@ruolo_richiesto("admin")  # <--- PROTETTO: Solo l'admin può accedere!
def nuovo():
    """Crea un nuovo ingrediente, protetto dallo stato vuoto del sistema."""
    if not ricetta_service.esistono_ricette():
        flash("La gestione degli ingredienti non è disponibile perché non ci sono ricette nel sistema.", "warning")
        return redirect(url_for("main.home"))

    dati, errori = {"nome": "", "unita": "g"}, {}
    if request.method == "POST":
        dati = {"nome": request.form.get("nome", "").strip(), "unita": request.form.get("unita", "")}
        try:
            ingrediente_service.crea(valida(IngredienteFormDTO, dati))
            flash(f"Ingrediente «{dati['nome']}» aggiunto.", "success")
            return redirect(url_for("ingredienti.nuovo"))
        except ValidazioneError as e:
            errori = e.errori
        except ConflittoError as e:
            errori = {"nome": e.message}
        return render_template("ingredienti/nuovo.html", dati=dati, errori=errori), 400
    return render_template("ingredienti/nuovo.html", dati=dati, errori=errori)


@ingredienti_bp.route("/importa", methods=["GET", "POST"])
@login_required
@ruolo_richiesto("admin")
def importa():
    if request.method == "POST":
        file = request.files.get("file_csv")
        if not file or not file.filename.endswith(".csv"):
            flash("Per favore, carica un file CSV valido.", "danger")
            return redirect(request.url)
            
        try:
            inseriti, saltati = ingrediente_service.importa_da_csv(file.stream)
            flash(f"Importazione completata! Aggiunti: {inseriti}. Saltati (già esistenti): {saltati}.", "success")
            return redirect(url_for("dispensa.elenco"))
        except Exception as e:
            flash(f"Errore durante l'importazione: {str(e)}", "danger")
            return redirect(request.url)
            
    return render_template("ingredienti/importa.html")
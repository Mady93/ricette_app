from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.container import ingrediente_service
from app.dto.ingrediente_dto import IngredienteFormDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, ValidazioneError
from app.utils.decorators import login_required

ingredienti_bp = Blueprint("ingredienti", __name__, url_prefix="/ingredienti")


@ingredienti_bp.route("/nuovo", methods=["GET", "POST"])
@login_required
def nuovo():
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

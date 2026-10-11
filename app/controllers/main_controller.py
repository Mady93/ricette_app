"""Controller delle pagine principali: home e profilo."""

from typing import Optional

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.container import dispensa_service, ricetta_service, auth_service
from app.dto.auth_dto import AggiornaProfiloDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, ValidazioneError
from app.utils import grafici
from app.utils.decorators import login_required

main_bp = Blueprint("main", __name__)


def _statistica_home() -> Optional[dict]:
    """Sceglie il grafico della home.

    Con una dispensa che combacia con qualche ricetta: quanto ti manca per cucinarle.
    Altrimenti (ospite, dispensa vuota): quante ricette ci sono per difficoltà.
    """
    if g.get("utente"):
        suggerimenti = dispensa_service.cosa_posso_cucinare(g.utente.id)[:5]
        if suggerimenti:
            voci = tuple((s.titolo, s.percentuale) for s in suggerimenti)
            return {
                "titolo": "Cosa puoi cucinare",
                "immagine": grafici.copertura_ricette(voci),
                "descrizione": "Ingredienti già in dispensa per ricetta: "
                               + ", ".join(f"{t} {p}%" for t, p in voci),
                "link": url_for("dispensa.cosa_cucinare"),
                "link_testo": "Vedi tutte",
            }

    facile, media, difficile = (ricetta_service.elenco("", d, None, 1).totale
                                for d in ("facile", "media", "difficile"))
    if facile + media + difficile == 0:
        return None
    return {
        "titolo": "Le ricette in numeri",
        "immagine": grafici.ricette_per_difficolta(facile, media, difficile),
        "descrizione": f"Ricette per difficoltà: {facile} facili, {media} medie, {difficile} difficili",
        "link": url_for("ricette.elenco"),
        "link_testo": "Sfoglia le ricette",
    }


@main_bp.route("/")
def home() -> str:
    """Home: hero, grafico statistico e passi."""
    return render_template("main/home.html", stat=_statistica_home())


@main_bp.route("/profilo", methods=["GET", "POST"])
@login_required
def profilo() -> str:
    """Pagina profilo dell'utente loggato con supporto alla modifica."""
    errori = {}
    dati = {"username": g.utente.username, "email": g.utente.email}

    if request.method == "POST":
        f = request.form
        dati = {"username": f.get("username", "").strip(), "email": f.get("email", "").strip()}
        try:
            dto = valida(AggiornaProfiloDTO, dati)
            # Aggiorna il profilo tramite il service
            utente_aggiornato = auth_service.aggiorna_profilo(g.utente.id, dto)
            # Aggiorna l'utente corrente in g per riflettere subito i cambiamenti
            g.utente = utente_aggiornato
            flash("Profilo aggiornato con successo!", "success")
            return redirect(url_for("main.profilo"))
        except ValidazioneError as e:
            errori = e.errori
        except ConflittoError as e:
            errori = {"generale": e.message}

    return render_template("main/profilo.html", dati=dati, errori=errori)
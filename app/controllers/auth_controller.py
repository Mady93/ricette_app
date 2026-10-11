import logging

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.container import auth_service
from app.dto.auth_dto import LoginDTO, RegistrazioneDTO
from app.dto.validazione import valida
from app.exceptions import ConflittoError, CredenzialiNonValideError, ValidazioneError
from app.extensions import limiter

log = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/registrati", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def registrati() -> tuple:
    """Gestisce la registrazione di un nuovo utente ed effettua l'accesso automatico."""
    dati: dict[str, str] = {"username": "", "email": ""}
    errori: dict = {}
    if request.method == "POST":
        f = request.form
        dati = {"username": f.get("username", "").strip(), "email": f.get("email", "").strip()}
        try:
            dto = valida(RegistrazioneDTO, {**dati, "password": f.get("password", ""),
                                            "conferma_password": f.get("conferma_password", "")})
            nuovo = auth_service.registra(dto)
            log.info("registrazione completata", extra={"evento": "registrazione", "utente_id": nuovo.id})
            
            # --- AUTO-LOGIN IMMEDIATO ---
            session.clear()  # anti session fixation
            session["utente_id"] = nuovo.id
            session.permanent = True
            
            flash(f"Benvenuto/a {nuovo.username}! Account creato con successo.", "success")
            return redirect(url_for("main.home"))
            
        except ValidazioneError as e:
            errori = e.errori
        except ConflittoError as e:
            errori = {"generale": e.message}
        return render_template("auth/registrati.html", dati=dati, errori=errori), 400
    return render_template("auth/registrati.html", dati=dati, errori=errori)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login() -> tuple:
    """Gestisce il login dell'utente."""
    if request.method == "POST":
        f = request.form
        identificativo = f.get("identificativo", "").strip()
        try:
            dto = valida(LoginDTO, {"identificativo": identificativo, "password": f.get("password", "")})
            utente = auth_service.login(dto)
        except (ValidazioneError, CredenzialiNonValideError):
            log.warning("login fallito", extra={"evento": "login_fallito"})
            return render_template("auth/login.html", identificativo=identificativo,
                                   errore="Username/email o password non corretti."), 401
        log.info("login riuscito", extra={"evento": "login_riuscito", "utente_id": utente.id})
        session.clear()                 # anti session fixation
        session["utente_id"] = utente.id
        session.permanent = True
        flash(f"Bentornato/a, {utente.username}!", "success")
        return redirect(url_for("main.home"))
    return render_template("auth/login.html", errore=None, identificativo="")


@auth_bp.route("/logout", methods=["POST"])
def logout() -> tuple:
    """Esegue il logout dell'utente corrente."""
    log.info("logout", extra={"evento": "logout"})
    session.clear()
    flash("Hai effettuato il logout.", "info")
    return redirect(url_for("main.home"))
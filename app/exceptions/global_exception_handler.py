"""Gestore globale degli errori (equivalente di @ControllerAdvice)."""
import logging

import mysql.connector
from flask import flash, redirect, render_template, url_for
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException

from app.exceptions.app_exceptions import AppError, NonAutenticatoError

log = logging.getLogger(__name__)


def _risposta(codice, messaggio):
    return render_template("errors/errore.html", codice=codice, messaggio=messaggio), codice


def register_error_handlers(app):
    @app.errorhandler(NonAutenticatoError)
    def non_autenticato(e):
        flash(e.message, "warning")
        return redirect(url_for("auth.login"))

    @app.errorhandler(AppError)
    def errore_applicativo(e):
        log.warning("%s: %s", type(e).__name__, e.message,
                    extra={"evento": type(e).__name__, "codice": e.status_code})
        return _risposta(e.status_code, e.message)

    @app.errorhandler(CSRFError)
    def errore_csrf(e):
        return _risposta(400, "Il modulo è scaduto o non è valido. Ricarica la pagina e riprova.")

    @app.errorhandler(mysql.connector.Error)
    def errore_database(e):
        log.exception("Errore database")           # dettagli solo nel log
        return _risposta(500, "Si è verificato un errore. Riprova più tardi.")

    @app.errorhandler(HTTPException)
    def errore_http(e):
        return _risposta(e.code, e.description)

    @app.errorhandler(Exception)
    def errore_generico(e):
        if app.debug:
            raise e                                 # in sviluppo vedi il traceback
        log.exception("Errore non gestito")
        return _risposta(500, "Si è verificato un errore. Riprova più tardi.")

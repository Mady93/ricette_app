"""Factory dell'applicazione Flask: configura estensioni, blueprint, hook e header di sicurezza."""

import logging
from typing import Any

from flask import Flask, Response, g, request, session
from mysql.connector import Error as MySQLError

from app import db
from app.config import Config
from app.models.utente import UtenteAnonimo
from .container import auth_service, ricetta_service
from app.controllers.admin_controller import admin_bp
from app.controllers.auth_controller import auth_bp
from .controllers.dispensa_controller import dispensa_bp
from app.controllers.ingredienti_controller import ingredienti_bp
from app.controllers.ricette_controller import ricette_bp
from app.controllers.main_controller import main_bp
from app.exceptions import RisorsaNonTrovataError
from app.exceptions.global_exception_handler import register_error_handlers
from app.extensions import csrf, limiter
from app.logging_config import configura_logging
from app.utils.filters import qta


def create_app(config_override: dict[str, Any] | None = None) -> Flask:
    """Crea e configura l'app Flask; config_override serve ai test per cambiare impostazioni."""
    app = Flask(__name__)

    # Carica la configurazione dalla classe Config (che legge il file .env)
    app.config.from_object(Config)
    if config_override:
        app.config.update(config_override)

    # <-- IN SVILUPPO PER EVITARE LA CACHE DEI TEMPLATE -->
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Senza SECRET_KEY sessioni e CSRF non sono sicure: meglio fermarsi subito
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY mancante nel file .env")

    # Inizializza logging, database e protezioni (CSRF e limite di richieste)
    configura_logging(app)
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Registra l'handler globale delle eccezioni (pagine di errore uniformi)
    register_error_handlers(app)

    # Collega i controller (blueprint) all'applicazione
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ricette_bp)
    app.register_blueprint(ingredienti_bp)
    app.register_blueprint(dispensa_bp)
    app.register_blueprint(admin_bp)

    # Rende disponibile il filtro |qta nei template Jinja
    app.add_template_filter(qta, "qta")

    @app.before_request
    def carica_utente() -> None:
        """Prima di ogni richiesta carica l'utente loggato (se c'è) in g.utente."""
        g.utente = None

        # I file statici non hanno bisogno dell'utente: evita query inutili
        if request.endpoint == "static":
            return

        utente_id = session.get("utente_id")
        if utente_id:
            try:
                g.utente = auth_service.get_utente(utente_id)
            except RisorsaNonTrovataError:
                # L'utente non esiste più nel database: la sessione non è valida
                session.clear()

    @app.context_processor
    def inietta_utente() -> dict[str, Any]:
        """Rende 'utente' e 'current_user' disponibili in tutti i template."""
        # Se nessuno è loggato usa l'utente anonimo (Null Object), così il template non va in errore
        u = g.get("utente") or UtenteAnonimo()
        return {
            "utente": u,
            "current_user": u,
        }

    @app.context_processor
    def inietta_ricette() -> dict[str, Any]:
        """Rende 'ha_ricette' disponibile in tutti i template (serve alla navbar e alla home)."""
        # Calcola il valore una sola volta per richiesta e lo conserva in g
        if "ha_ricette" not in g:
            try:
                g.ha_ricette = ricetta_service.esistono_ricette()
            except MySQLError:
                # Se il database non risponde, scrive il dettaglio nei log e nasconde il link
                logging.getLogger(__name__).exception("Impossibile verificare le ricette")
                g.ha_ricette = False
        return {"ha_ricette": g.ha_ricette}

    @app.after_request
    def header_sicurezza(resp: Response) -> Response:
        """Aggiunge gli header di sicurezza a ogni risposta HTTP."""
        # Impedisce al browser di indovinare il tipo di un file
        resp.headers["X-Content-Type-Options"] = "nosniff"
        # Vieta di incorporare il sito in un iframe (difesa dal clickjacking)
        resp.headers["X-Frame-Options"] = "DENY"
        # Invia il referrer solo verso lo stesso sito
        resp.headers["Referrer-Policy"] = "same-origin"
        # Politica CSP: permette risorse dal sito, da jsDelivr (Bootstrap), Google Fonts e file multimediali locali
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "media-src 'self'; "
            "img-src 'self' data:; frame-ancestors 'none'; "
            "form-action 'self'; base-uri 'self'"
        )
        # HSTS (forza HTTPS) solo quando il cookie di sessione è marcato Secure, cioè in produzione
        if app.config.get("SESSION_COOKIE_SECURE"):
            resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return resp

    return app
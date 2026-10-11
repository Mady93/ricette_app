from pathlib import Path
import re

import mysql.connector
from mysql.connector import Error
from flask import current_app, g


def get_db():
    """Una connessione per richiesta, riusata finché la richiesta è viva."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            charset="utf8mb4",
            connection_timeout=5,
            autocommit=False,
        )
    return g.db


def close_db(errore=None):
    db = g.pop("db", None)
    if db is not None and db.is_connected():
        db.close()


def _crea_database_se_manca(app):
    """Crea il database configurato se non esiste."""
    nome_db = app.config.get("DB_NAME")

    if not nome_db or not nome_db.strip():
        raise RuntimeError(
            "DB_NAME mancante nel file .env. "
            "Impossibile inizializzare il database."
        )

    if not re.fullmatch(r"[A-Za-z0-9_]+", nome_db):
        raise ValueError("DB_NAME contiene caratteri non consentiti.")

    connessione = None
    cursore = None

    try:
        connessione = mysql.connector.connect(
            host=app.config["DB_HOST"],
            port=app.config["DB_PORT"],
            user=app.config["DB_USER"],
            password=app.config["DB_PASSWORD"],
            connection_timeout=5,
        )

        cursore = connessione.cursor()
        cursore.execute(
            f"CREATE DATABASE IF NOT EXISTS `{nome_db}` "
            "CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci"
        )

        app.logger.info(
            "Database '%s' verificato o creato.",
            nome_db,
        )

    except Error:
        app.logger.exception(
            "Impossibile verificare o creare il database."
        )
        raise

    finally:
        if cursore is not None:
            cursore.close()

        if connessione is not None and connessione.is_connected():
            connessione.close()


def _crea_tabelle_se_mancano(app):
    """Esegue lo schema SQL nel database indicato nel .env."""
    nome_db = app.config["DB_NAME"]

    percorso_schema = (
        Path(__file__).resolve().parent.parent
        / "sql"
        / "02_schema.sql"
    )

    if not percorso_schema.is_file():
        raise FileNotFoundError(
            f"Schema SQL non trovato: {percorso_schema}"
        )

    schema = percorso_schema.read_text(encoding="utf-8")

    connessione = None
    cursore = None

    try:
        connessione = mysql.connector.connect(
            host=app.config["DB_HOST"],
            port=app.config["DB_PORT"],
            user=app.config["DB_USER"],
            password=app.config["DB_PASSWORD"],
            database=nome_db,
            charset="utf8mb4",
            connection_timeout=5,
            autocommit=True,
        )

        cursore = connessione.cursor()

        for istruzione in schema.split(";"):
            istruzione = istruzione.strip()

            if istruzione:
                cursore.execute(istruzione)

        app.logger.info(
            "Schema del database '%s' verificato.",
            nome_db,
        )

    except (Error, OSError):
        app.logger.exception(
            "Impossibile inizializzare lo schema del database '%s'.",
            nome_db,
        )
        raise

    finally:
        if cursore is not None:
            cursore.close()

        if connessione is not None and connessione.is_connected():
            connessione.close()


def init_app(app):
    """Inizializza database e tabelle all'avvio dell'applicazione."""
    _crea_database_se_manca(app)
    _crea_tabelle_se_mancano(app)
    app.teardown_appcontext(close_db)

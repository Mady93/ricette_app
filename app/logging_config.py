"""Logging strutturato (una riga JSON per evento) su file con rotazione + console."""
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from flask import g, has_request_context, request

_STANDARD = set(vars(logging.LogRecord("", 0, "", 0, "", (), None))) | {"message", "asctime", "taskName"}
_NOSTRO = "_nostro_handler"


class ContestoRichiestaFilter(logging.Filter):
    """Aggiunge a OGNI log, in automatico, request_id / ip / utente / percorso."""

    def filter(self, record):
        if has_request_context():
            valori = {
                "request_id": g.get("request_id"),
                "ip": request.remote_addr,
                "metodo": request.method,
                "percorso": request.path,                       # mai la query string
                "utente_id": g.utente.id if g.get("utente") else None,
            }
            for chiave, valore in valori.items():
                if not hasattr(record, chiave):                 # non sovrascrive gli extra espliciti
                    setattr(record, chiave, valore)
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        dati = {
            "ts": datetime.fromtimestamp(record.created, timezone.utc).isoformat(timespec="milliseconds"),
            "livello": record.levelname,
            "logger": record.name,
            "messaggio": record.getMessage(),
        }
        for chiave, valore in vars(record).items():
            if chiave not in _STANDARD and not chiave.startswith("_") and valore is not None:
                dati[chiave] = valore
        if record.exc_info:
            dati["eccezione"] = self.formatException(record.exc_info)
        return json.dumps(dati, ensure_ascii=False, default=str)


def chiudi_logging():
    logger = logging.getLogger("app")
    for h in list(logger.handlers):
        if getattr(h, _NOSTRO, False):
            logger.removeHandler(h)
            h.close()


def configura_logging(app):
    chiudi_logging()                                            # evita handler doppi
    logger = logging.getLogger("app")                           # = app.logger e tutti i moduli app.*
    logger.setLevel(app.config["LOG_LEVEL"])

    filtro = ContestoRichiestaFilter()
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
    handlers = [console]

    if app.config["LOG_TO_FILE"]:
        os.makedirs(app.config["LOG_DIR"], exist_ok=True)
        file_h = RotatingFileHandler(
            os.path.join(app.config["LOG_DIR"], "app.log"),
            maxBytes=app.config["LOG_MAX_BYTES"], backupCount=app.config["LOG_BACKUPS"], encoding="utf-8")
        file_h.setFormatter(JsonFormatter())
        handlers.append(file_h)

    for h in handlers:
        h.addFilter(filtro)
        setattr(h, _NOSTRO, True)
        logger.addHandler(h)

    access = logging.getLogger("app.access")

    @app.before_request
    def _inizio():
        g.request_id = uuid.uuid4().hex[:12]
        g.t0 = time.perf_counter()

    @app.after_request
    def _fine(resp):
        resp.headers["X-Request-ID"] = g.get("request_id", "")
        if request.endpoint != "static":
            livello = logging.ERROR if resp.status_code >= 500 else \
                logging.WARNING if resp.status_code >= 400 else logging.INFO
            access.log(livello, "richiesta", extra={
                "stato": resp.status_code,
                "durata_ms": round((time.perf_counter() - g.get("t0", time.perf_counter())) * 1000, 1),
            })
        return resp

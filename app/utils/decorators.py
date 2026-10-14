from functools import wraps

from flask import g

from app.exceptions import NonAutenticatoError, NonAutorizzatoError


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.get("utente") is None:
            raise NonAutenticatoError()
        return f(*args, **kwargs)
    return wrapper


def ruolo_richiesto(ruolo):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if g.utente.ruolo != ruolo:
                raise NonAutorizzatoError()
            return f(*args, **kwargs)
        return wrapper
    return decorator


# Scorciatoia per le rotte riservate agli amministratori:
# non loggato -> redirect al login, loggato ma non admin -> 403.
admin_required = ruolo_richiesto("admin")

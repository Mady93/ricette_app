class AppError(Exception):
    """Base di tutte le eccezioni applicative."""
    status_code = 500
    message = "Errore interno."

    def __init__(self, message=None):
        super().__init__(message or self.message)
        self.message = message or self.message


class ValidazioneError(AppError):
    status_code = 400
    message = "Dati non validi."

    def __init__(self, errori: dict, message=None):
        super().__init__(message)
        self.errori = errori          # {"campo": "messaggio"}


class CredenzialiNonValideError(AppError):
    status_code = 401
    message = "Credenziali non valide."


class NonAutenticatoError(AppError):
    status_code = 401
    message = "Devi effettuare il login."


class NonAutorizzatoError(AppError):
    status_code = 403
    message = "Non hai i permessi per questa operazione."


class RisorsaNonTrovataError(AppError):
    status_code = 404
    message = "Risorsa non trovata."


class ConflittoError(AppError):
    status_code = 409
    message = "Conflitto con i dati esistenti."

import mysql.connector

from app.db import get_db
from app.models.utente import Utente

_COLONNE = "id, username, email, password_hash, ruolo, creato_il"


class UtenteRepository:
    """Solo query SQL parametrizzate (%s). Nessuna regola di business."""

    def _uno(self, query, params):
        cursor = get_db().cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            riga = cursor.fetchone()
            return Utente(**riga) if riga else None
        finally:
            cursor.close()

    def find_by_id(self, utente_id):
        return self._uno(f"SELECT {_COLONNE} FROM utenti WHERE id = %s", (utente_id,))

    def find_by_identificativo(self, identificativo):
        return self._uno(
            f"SELECT {_COLONNE} FROM utenti WHERE username = %s OR email = %s LIMIT 1",
            (identificativo, identificativo.lower()),
        )

    def exists_by_username(self, username):
        return self._esiste("SELECT 1 FROM utenti WHERE username = %s LIMIT 1", (username,))

    def exists_by_email(self, email):
        return self._esiste("SELECT 1 FROM utenti WHERE email = %s LIMIT 1", (email,))

    def _esiste(self, query, params):
        cursor = get_db().cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def save(self, utente: Utente) -> int:
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO utenti (username, email, password_hash, ruolo) VALUES (%s, %s, %s, %s)",
                (utente.username, utente.email, utente.password_hash, utente.ruolo),
            )
            db.commit()
            return cursor.lastrowid
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cursor.close()

    def update_profilo(self, utente_id: int, username: str, email: str) -> None:
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE utenti SET username = %s, email = %s WHERE id = %s",
                (username, email, utente_id),
            )
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cursor.close()

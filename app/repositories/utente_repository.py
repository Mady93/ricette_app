import mysql.connector

from app.db import get_db
from app.models.admin import UtenteRiepilogo
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

    # ---- area admin ----
    def find_all_con_ricette(self):
        """Tutti gli utenti, con il numero di ricette scritte da ciascuno."""
        cursor = get_db().cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT u.id, u.username, u.email, u.ruolo, u.creato_il, COUNT(r.id) AS n_ricette "
                "FROM utenti u LEFT JOIN ricette r ON r.utente_id = u.id "
                "GROUP BY u.id, u.username, u.email, u.ruolo, u.creato_il "
                "ORDER BY u.username"
            )
            return [UtenteRiepilogo(**r) for r in cursor.fetchall()]
        finally:
            cursor.close()

    def conta(self) -> int:
        return self._numero("SELECT COUNT(*) FROM utenti")

    def conta_admin(self) -> int:
        return self._numero("SELECT COUNT(*) FROM utenti WHERE ruolo = 'admin'")

    def _numero(self, query):
        cursor = get_db().cursor()
        try:
            cursor.execute(query)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def update_ruolo(self, utente_id: int, ruolo: str) -> None:
        self._scrivi("UPDATE utenti SET ruolo = %s WHERE id = %s", (ruolo, utente_id))

    def delete(self, utente_id: int) -> None:
        # le sue ricette restano (utente_id -> NULL), la sua dispensa sparisce (ON DELETE CASCADE)
        self._scrivi("DELETE FROM utenti WHERE id = %s", (utente_id,))

    def _scrivi(self, query, params):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cursor.close()

import mysql.connector

from app.db import get_db
from app.models.dispensa import Suggerimento, VoceDispensa


class DispensaRepository:
    def find_by_utente(self, utente_id):
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT i.id AS ingrediente_id, i.nome, i.unita_base, d.quantita "
                "FROM dispensa d JOIN ingredienti i ON i.id = d.ingrediente_id "
                "WHERE d.utente_id = %s ORDER BY i.nome",
                (utente_id,),
            )
            return [VoceDispensa(**r) for r in cur.fetchall()]
        finally:
            cur.close()

    def upsert(self, utente_id, ingrediente_id, quantita):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO dispensa (utente_id, ingrediente_id, quantita) VALUES (%s, %s, %s) AS nuovo "
                "ON DUPLICATE KEY UPDATE quantita = nuovo.quantita",
                (utente_id, ingrediente_id, quantita),
            )
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

    def delete(self, utente_id, ingrediente_id):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM dispensa WHERE utente_id = %s AND ingrediente_id = %s",
                        (utente_id, ingrediente_id))
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

    def possedute_per_ricetta(self, utente_id, ricetta_id):
        cur = get_db().cursor()
        try:
            cur.execute(
                "SELECT d.ingrediente_id, d.quantita FROM dispensa d "
                "JOIN ricetta_ingredienti ri ON ri.ingrediente_id = d.ingrediente_id "
                "WHERE d.utente_id = %s AND ri.ricetta_id = %s",
                (utente_id, ricetta_id),
            )
            return {r[0]: r[1] for r in cur.fetchall()}
        finally:
            cur.close()

    def suggerimenti(self, utente_id, limite):
        """Una sola query: per ogni ricetta conta gli ingredienti totali e quelli in dispensa."""
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT r.id, r.titolo, r.minuti, r.difficolta, "
                "       COUNT(ri.ingrediente_id) AS totale, "
                "       SUM(CASE WHEN d.quantita >= ri.quantita THEN 1 ELSE 0 END) AS posseduti "
                "FROM ricette r "
                "JOIN ricetta_ingredienti ri ON ri.ricetta_id = r.id "
                "LEFT JOIN dispensa d ON d.ingrediente_id = ri.ingrediente_id AND d.utente_id = %s "
                "GROUP BY r.id, r.titolo, r.minuti, r.difficolta "
                "HAVING posseduti > 0 "
                "ORDER BY posseduti / totale DESC, totale ASC, r.titolo "
                "LIMIT %s",
                (utente_id, limite),
            )
            return [Suggerimento(r["id"], r["titolo"], r["minuti"], r["difficolta"],
                                 int(r["totale"]), int(r["posseduti"])) for r in cur.fetchall()]
        finally:
            cur.close()

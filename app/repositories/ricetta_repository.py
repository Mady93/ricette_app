import mysql.connector

from app.db import get_db
from app.models.ricetta import Ricetta, RicettaSintesi, RigaRicetta

_COLONNE = "id, utente_id, titolo, descrizione, istruzioni, porzioni, minuti, difficolta, creato_il"


def _escape_like(testo):
    return testo.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _where(q, difficolta, max_minuti):
    """Le clausole sono costanti: solo i VALORI viaggiano come parametri."""
    clausole, params = [], []
    if q:
        clausole.append("(MATCH(titolo, descrizione) AGAINST (%s IN NATURAL LANGUAGE MODE) OR titolo LIKE %s)")
        params += [q, f"%{_escape_like(q)}%"]
    if difficolta:
        clausole.append("difficolta = %s")
        params.append(difficolta)
    if max_minuti:
        clausole.append("minuti <= %s")
        params.append(max_minuti)
    return ("WHERE " + " AND ".join(clausole)) if clausole else "", params


class RicettaRepository:
    def conta(self, q, difficolta, max_minuti):
        where, params = _where(q, difficolta, max_minuti)
        cur = get_db().cursor()
        try:
            cur.execute(f"SELECT COUNT(*) FROM ricette {where}", tuple(params))
            return cur.fetchone()[0]
        finally:
            cur.close()

    def cerca(self, q, difficolta, max_minuti, limite, offset):
        where, params = _where(q, difficolta, max_minuti)
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT id, titolo, descrizione, porzioni, minuti, difficolta FROM ricette "
                f"{where} ORDER BY creato_il DESC, id DESC LIMIT %s OFFSET %s",
                tuple(params + [limite, offset]),
            )
            return [RicettaSintesi(**r) for r in cur.fetchall()]
        finally:
            cur.close()

    def find_by_id(self, ricetta_id):
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(f"SELECT {_COLONNE} FROM ricette WHERE id = %s", (ricetta_id,))
            riga = cur.fetchone()
            return Ricetta(**riga) if riga else None
        finally:
            cur.close()

    def righe_di(self, ricetta_id):
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT i.id AS ingrediente_id, i.nome, i.unita_base, ri.quantita "
                "FROM ricetta_ingredienti ri JOIN ingredienti i ON i.id = ri.ingrediente_id "
                "WHERE ri.ricetta_id = %s ORDER BY i.nome",
                (ricetta_id,),
            )
            return [RigaRicetta(**r) for r in cur.fetchall()]
        finally:
            cur.close()

    def save(self, r: Ricetta, righe):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO ricette (utente_id, titolo, descrizione, istruzioni, porzioni, minuti, difficolta) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (r.utente_id, r.titolo, r.descrizione, r.istruzioni, r.porzioni, r.minuti, r.difficolta),
            )
            nuovo_id = cur.lastrowid
            cur.executemany(
                "INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita) VALUES (%s, %s, %s)",
                [(nuovo_id, i, q) for i, q in righe],
            )
            db.commit()                      # ricetta + ingredienti: tutto o niente
            return nuovo_id
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

    def update(self, r: Ricetta, righe):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "UPDATE ricette SET titolo=%s, descrizione=%s, istruzioni=%s, porzioni=%s, minuti=%s, "
                "difficolta=%s WHERE id=%s",
                (r.titolo, r.descrizione, r.istruzioni, r.porzioni, r.minuti, r.difficolta, r.id),
            )
            cur.execute("DELETE FROM ricetta_ingredienti WHERE ricetta_id = %s", (r.id,))
            cur.executemany(
                "INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita) VALUES (%s, %s, %s)",
                [(r.id, i, q) for i, q in righe],
            )
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

    def delete(self, ricetta_id):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM ricette WHERE id = %s", (ricetta_id,))
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

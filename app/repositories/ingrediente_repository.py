import mysql.connector

from app.db import get_db
from app.models.ingrediente import Ingrediente


class IngredienteRepository:
    def find_all(self):
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute("SELECT id, nome, unita_base FROM ingredienti ORDER BY nome")
            return [Ingrediente(**r) for r in cur.fetchall()]
        finally:
            cur.close()

    def find_ids_esistenti(self, ids):
        if not ids:
            return set()
        segnaposto = ", ".join(["%s"] * len(ids))          # solo %s, mai valori nella stringa
        cur = get_db().cursor()
        try:
            cur.execute(f"SELECT id FROM ingredienti WHERE id IN ({segnaposto})", tuple(ids))
            return {r[0] for r in cur.fetchall()}
        finally:
            cur.close()

    def exists_by_nome(self, nome):
        cur = get_db().cursor()
        try:
            cur.execute("SELECT 1 FROM ingredienti WHERE nome = %s LIMIT 1", (nome,))
            return cur.fetchone() is not None
        finally:
            cur.close()

    def save(self, nome, unita):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO ingredienti (nome, unita_base) VALUES (%s, %s)", (nome, unita))
            db.commit()
            return cur.lastrowid
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

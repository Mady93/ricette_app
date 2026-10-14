import mysql.connector

from app.db import get_db
from app.models.admin import IngredienteRiepilogo
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

    # ---- area admin ----
    def find_by_id(self, ingrediente_id):
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute("SELECT id, nome, unita_base FROM ingredienti WHERE id = %s", (ingrediente_id,))
            riga = cur.fetchone()
            return Ingrediente(**riga) if riga else None
        finally:
            cur.close()

    def find_all_con_utilizzi(self):
        """Catalogo completo con, per ogni ingrediente, quante ricette e quante dispense lo usano."""
        cur = get_db().cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT i.id, i.nome, i.unita_base, "
                "(SELECT COUNT(*) FROM ricetta_ingredienti ri WHERE ri.ingrediente_id = i.id) AS n_ricette, "
                "(SELECT COUNT(*) FROM dispensa d WHERE d.ingrediente_id = i.id) AS n_dispense "
                "FROM ingredienti i ORDER BY i.nome"
            )
            return [IngredienteRiepilogo(**r) for r in cur.fetchall()]
        finally:
            cur.close()

    def utilizzi(self, ingrediente_id):
        """(n. ricette, n. dispense) che usano l'ingrediente."""
        cur = get_db().cursor()
        try:
            cur.execute(
                "SELECT (SELECT COUNT(*) FROM ricetta_ingredienti WHERE ingrediente_id = %s), "
                "(SELECT COUNT(*) FROM dispensa WHERE ingrediente_id = %s)",
                (ingrediente_id, ingrediente_id),
            )
            n_ricette, n_dispense = cur.fetchone()
            return n_ricette, n_dispense
        finally:
            cur.close()

    def exists_by_nome_escluso(self, nome, ingrediente_id):
        """Esiste un ALTRO ingrediente con questo nome? (serve alla rinomina)"""
        cur = get_db().cursor()
        try:
            cur.execute("SELECT 1 FROM ingredienti WHERE nome = %s AND id <> %s LIMIT 1", (nome, ingrediente_id))
            return cur.fetchone() is not None
        finally:
            cur.close()

    def update(self, ingrediente_id, nome, unita):
        self._scrivi("UPDATE ingredienti SET nome = %s, unita_base = %s WHERE id = %s",
                     (nome, unita, ingrediente_id))

    def delete(self, ingrediente_id):
        # se compare in una ricetta, MySQL rifiuta (ON DELETE RESTRICT); dalle dispense sparisce (CASCADE)
        self._scrivi("DELETE FROM ingredienti WHERE id = %s", (ingrediente_id,))

    def conta(self):
        return self._numero("SELECT COUNT(*) FROM ingredienti")

    def conta_inutilizzati(self):
        return self._numero(
            "SELECT COUNT(*) FROM ingredienti i "
            "WHERE NOT EXISTS (SELECT 1 FROM ricetta_ingredienti ri WHERE ri.ingrediente_id = i.id)"
        )

    def _numero(self, query):
        cur = get_db().cursor()
        try:
            cur.execute(query)
            return cur.fetchone()[0]
        finally:
            cur.close()

    def _scrivi(self, query, params):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute(query, params)
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            raise
        finally:
            cur.close()

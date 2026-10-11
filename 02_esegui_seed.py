from pathlib import Path
import os
import mysql.connector
from dotenv import load_dotenv
from argon2 import PasswordHasher

load_dotenv()

config = {
    "host": os.getenv("DB_HOST", "127.0.0.1").strip(),
    "port": int(os.getenv("DB_PORT", "3306").strip()),
    "user": os.getenv("DB_USER", "root").strip(),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ricette_db").strip(),
}

script_path = Path(__file__).parent / "sql" / "03_seed.sql"
sql_script = script_path.read_text(encoding="utf-8")

connection = mysql.connector.connect(**config)

try:
    cursor = connection.cursor()

    # 1. Inserisce l'utente admin se non esiste già (con password 'Admin_123' protetta con Argon2id)
    ph = PasswordHasher()
    admin_password_hash = ph.hash("Admin_123")
    
    cursor.execute(
        """
        INSERT INTO utenti (username, email, password_hash, ruolo)
        SELECT 'admin', 'admin@ricette.local', %s, 'admin'
        FROM DUAL
        WHERE NOT EXISTS (
            SELECT 1 FROM utenti WHERE username = 'admin'
        );
        """,
        (admin_password_hash,)
    )
    connection.commit()

    # 2. Recupera l'ID dell'admin appena creato o esistente
    cursor.execute("SELECT id FROM utenti WHERE username = 'admin'")
    result = cursor.fetchone()
    admin_id = result[0] if isinstance(result, tuple) else result['id']

    # 3. Sostituisce i "NULL" riferiti all'utente_id delle ricette con l'ID dell'admin reale
    sql_script_modificato = sql_script.replace("SELECT NULL, '", f"SELECT {admin_id}, '")

    # 4. Esegue lo script di seed modificato (statement per statement)
    for statement in sql_script_modificato.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    connection.commit()
    print(f"Seed eseguito correttamente. Tutte le 100 ricette sono state associate all'admin (ID: {admin_id}).")

    # Verifica le ricette presenti nel database.
    cursor.execute("""
        SELECT id, utente_id, titolo, codice_seed
        FROM ricette
        ORDER BY id
    """)

    print("\nRicette presenti nel database:")
    for riga in cursor.fetchall():
        print(riga)

except Exception as error:
    connection.rollback()
    print(f"Errore durante il seed: {error}")
    raise

finally:
    cursor.close()
    connection.close()
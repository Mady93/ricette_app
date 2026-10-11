from app import create_app
from app import db

app = create_app()

with app.app_context():
    connection = db.get_db()
    cursor = connection.cursor()
    
    try:
        # 1. Inserisce l'utente admin se non esiste già
        cursor.execute(
            """
            INSERT INTO utenti (username, email, password_hash, ruolo)
            SELECT 'admin', 'admin@ricette.local', '$argon2id$v=19$m=65536,t=3,p=4$+ZDMV2nVBmAJOFXbFpiIxQ$8eGFT8gb+YSzIWnxqOhiuuAZHEajCwVgMkTd4frDOdY', 'admin'
            FROM DUAL
            WHERE NOT EXISTS (
                SELECT 1 FROM utenti WHERE username = 'admin'
            );
            """
        )
        
        # 2. Associa tutte le ricette senza proprietario all'admin
        cursor.execute(
            """
            UPDATE ricette 
            SET utente_id = (SELECT id FROM utenti WHERE username = 'admin') 
            WHERE utente_id IS NULL;
            """
        )
        
        connection.commit()
        print("Utente admin creato e ricette associate con successo!")
    except Exception as e:
        connection.rollback()
        print(f"Errore: {e}")
    finally:
        cursor.close()
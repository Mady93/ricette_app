# 🍳 Dispensa & Ricette

Applicazione web professionale sviluppata in **Flask** che risponde a una domanda semplice: *"Cosa cucino con quello che ho in casa?"*

L'utente inserisce gli ingredienti disponibili in dispensa (con relative quantità) e l'applicazione si occupa di:
- ordinare le ricette per **percentuale di ingredienti già disponibili**;
- mostrare per ogni ricetta **cosa manca** e generare la **lista della spesa in formato CSV** protetta da CSV injection;
- permettere di **scalare le quantità** in base al numero di porzioni desiderate.

---

## 🚀 Funzionalità Principali

| Area | Cosa fa |
|---|---|
| **Account** | Registrazione con login automatico, login flessibile con username o email, gestione profilo utente e logout. |
| **Ricette** | Elenco paginato (9 per pagina) con ricerca testuale, filtri per difficoltà e tempo massimo; dettaglio ricetta con porzioni scalabili; creazione, modifica ed eliminazione. |
| **Cataloghi & Admin** | Catalogo ingredienti condiviso; inserimento e importazione protetti e riservati esclusivamente agli utenti con ruolo `admin`. |
| **Dispensa Personale** | Gestione della dispensa dell'utente con autocomplete interattivo degli ingredienti, impostazione/aggiornamento quantità e rimozione. |
| **Cosa Cucinare?** | Algoritmo di suggerimento intelligente con ricette ordinate per copertura degli ingredienti (100% = pronte da cucinare). |
| **Lista della Spesa** | Download immediato della lista in formato CSV con i soli ingredienti mancanti calibrati sulle porzioni scelte. |
| **Home Statistica** | Grafico dinamico generato tramite Matplotlib e incorporato come immagine PNG (data URI) per rispettare la CSP. |

---

## 🏗️ Architettura del Sistema

L'applicazione segue un'architettura a layer rigorosa e modulare[cite: 1]:

```text
Browser → Controller → Service → Repository → MySQL
             │            │
             └── DTO ─────┘   (dati validati in ingresso con Pydantic)
```

- **Controller**: gestiscono le richieste HTTP tramite Blueprint e restituiscono le viste. Nessuna logica di business risiede qui.
- **DTO (Data Transfer Objects)**: validano e normalizzano i dati in ingresso dai moduli prima di inoltrarli ai servizi.
- **Service**: applicano le regole di business (permessi, verifica degli ingredienti, calcolo porzioni e suggerimenti)[cite: 1].
- **Repository**: eseguono esclusivamente query SQL parametrizzate in sicurezza[cite: 1].
- **Container**: gestisce manualmente l'iniezione e il collegamento delle dipendenze[cite: 1].

Visualizzazione grafica dell'architettura e dello schema relazionale:
- **Architettura a layer**: `docs/architettura.png`[cite: 1]
- **Schema ER del database**: `docs/database.png`[cite: 1]

---

## 🛠️ Requisiti di Sistema

- **Python**: 3.10 o superiore[cite: 1]
- **MySQL**: 8.0.19 o superiore (richiesto per query avanzate di gestione dispensa)[cite: 1]

---

## ⚙️ Installazione e Configurazione

### 1. Clonazione e Ambiente Virtuale

Crea e attiva un ambiente virtuale Python:

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. Installazione delle Dipendenze

Installa le dipendenze necessarie per eseguire l'applicazione:

```bash
pip install -r requirements.txt
```

### 3. Configurazione delle Variabili d'Ambiente

Copia il file di esempio `.env.example` in `.env` e compila i parametri di connessione al database e le altre variabili richieste:

```bash
cp .env.example .env
```

Genera una chiave sicura per `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia la chiave generata nel file `.env`, assegnandola alla variabile `SECRET_KEY`.

### 4. Inizializzazione del Database

All'avvio, l'applicazione crea automaticamente lo schema delle tabelle, a condizione che l'utente MySQL disponga dei permessi `CREATE`.

Per popolare il catalogo iniziale e caricare le ricette di esempio, esegui lo script SQL:

```bash
mysql -u [tuo_utente] -p [tuo_db] < sql/03_seed.sql
```

> **Nota sui permessi di amministrazione:** la registrazione standard crea utenti con ruolo `utente`. Per promuovere un utente ad amministratore e abilitare la gestione degli ingredienti, esegui la seguente query sul database:

```sql
UPDATE utenti
SET ruolo = 'admin'
WHERE username = 'tuo_username';
```

Sostituisci `tuo_username` con il nome utente effettivo dell'account da promuovere.

---

## 🏃‍♂️ Avvio dell'Applicazione

Avvia l'applicazione eseguendo:

```bash
python run.py
```

Apri il browser e visita il seguente indirizzo:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Esecuzione dei Test

I test unitari e di integrazione sono realizzati con `pytest` e utilizzano repository in memoria (`tests/fakes.py`), evitando dipendenze dirette da MySQL durante l'esecuzione dei test.

Installa le dipendenze di sviluppo:

```bash
pip install -r requirements-dev.txt
```

Esegui la suite di test:

```bash
pytest
```

---

## 🔒 Sicurezza e Conformità

L'applicazione integra diverse misure di sicurezza:

- **Password:** hashing sicuro tramite l'algoritmo **Argon2id**.
- **CSP (Content Security Policy):** direttive di sicurezza restrittive che bloccano script e stili inline. L'interfaccia e i grafici sono progettati per rispettare questa policy.
- **Protezione CSRF:** protezione attiva su tutti i moduli tramite **Flask-WTF**.
- **Rate Limiting:** protezione in memoria contro gli attacchi di forza bruta sulle funzionalità di login e registrazione.
- **Prevenzione CSV Injection:** protezione integrata nell'esportazione dei dati tabulari.

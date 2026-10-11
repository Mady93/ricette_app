CREATE TABLE IF NOT EXISTS utenti (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  username      VARCHAR(30)  NOT NULL UNIQUE,
  email         VARCHAR(150) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  ruolo         ENUM('utente','admin') NOT NULL DEFAULT 'utente',
  creato_il     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ingredienti (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nome       VARCHAR(100) NOT NULL UNIQUE,
  unita_base ENUM('g','ml','pz') NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ricette (
  id INT AUTO_INCREMENT PRIMARY KEY,
  utente_id INT NULL,
  codice_seed VARCHAR(50) NULL UNIQUE,
  titolo VARCHAR(150) NOT NULL,
  descrizione TEXT,
  istruzioni  TEXT NOT NULL,
  porzioni    TINYINT UNSIGNED NOT NULL DEFAULT 4,
  minuti      SMALLINT UNSIGNED NOT NULL,
  difficolta  ENUM('facile','media','difficile') NOT NULL DEFAULT 'facile',
  creato_il   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_ricette_utente (utente_id),
  FULLTEXT INDEX ft_ricette (titolo, descrizione),
  CONSTRAINT fk_ricette_utente FOREIGN KEY (utente_id)
    REFERENCES utenti(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ricetta_ingredienti (
  ricetta_id     INT NOT NULL,
  ingrediente_id INT NOT NULL,
  quantita       DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (ricetta_id, ingrediente_id),
  INDEX idx_ri_ingrediente (ingrediente_id),
  CONSTRAINT fk_ri_ricetta FOREIGN KEY (ricetta_id)
    REFERENCES ricette(id) ON DELETE CASCADE,
  CONSTRAINT fk_ri_ingrediente FOREIGN KEY (ingrediente_id)
    REFERENCES ingredienti(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dispensa (
  utente_id      INT NOT NULL,
  ingrediente_id INT NOT NULL,
  quantita       DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (utente_id, ingrediente_id),
  CONSTRAINT fk_disp_utente FOREIGN KEY (utente_id)
    REFERENCES utenti(id) ON DELETE CASCADE,
  CONSTRAINT fk_disp_ingrediente FOREIGN KEY (ingrediente_id)
    REFERENCES ingredienti(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS preferiti (
  utente_id  INT NOT NULL,
  ricetta_id INT NOT NULL,
  PRIMARY KEY (utente_id, ricetta_id),
  CONSTRAINT fk_pref_utente FOREIGN KEY (utente_id)
    REFERENCES utenti(id) ON DELETE CASCADE,
  CONSTRAINT fk_pref_ricetta FOREIGN KEY (ricetta_id)
    REFERENCES ricette(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS piano_pasti (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  utente_id  INT NOT NULL,
  ricetta_id INT NOT NULL,
  giorno     DATE NOT NULL,
  pasto      ENUM('colazione','pranzo','cena') NOT NULL,
  UNIQUE KEY uq_piano (utente_id, giorno, pasto),
  CONSTRAINT fk_piano_utente FOREIGN KEY (utente_id)
    REFERENCES utenti(id) ON DELETE CASCADE,
  CONSTRAINT fk_piano_ricetta FOREIGN KEY (ricetta_id)
    REFERENCES ricette(id) ON DELETE CASCADE
) ENGINE=InnoDB;

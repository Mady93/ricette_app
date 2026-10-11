-- Dispensa & Ricette: seed idempotente di 100 ricette.
-- Compatibile con esegui_seed.py che divide il file sul carattere punto e virgola.
-- Non cancella dati e non modifica ricette personali (codice_seed NULL).
START TRANSACTION;

-- Garantisce la presenza di tutti gli ingredienti usati dalle 100 ricette.
INSERT IGNORE INTO ingredienti (nome, unita_base) VALUES
('Acciughe', 'g'),
('Acqua', 'ml'),
('Aglio', 'pz'),
('Avocado', 'pz'),
('Banane', 'pz'),
('Basilico', 'g'),
('Besciamella', 'g'),
('Broccoli', 'g'),
('Brodo di carne', 'ml'),
('Brodo vegetale', 'ml'),
('Bucatini', 'g'),
('Burro', 'g'),
('Cacao amaro', 'g'),
('Caffè', 'ml'),
('Cannella', 'g'),
('Capperi', 'g'),
('Carota', 'g'),
('Cavolfiore', 'g'),
('Ceci cotti', 'g'),
('Cetriolo', 'g'),
('Cioccolato fondente', 'g'),
('Cipolla', 'g'),
('Couscous', 'g'),
('Fagioli cannellini', 'g'),
('Farina', 'g'),
('Feta', 'g'),
('Fragole', 'g'),
('Funghi', 'g'),
('Gamberi', 'g'),
('Gnocchi di patate', 'g'),
('Gorgonzola', 'g'),
('Guanciale', 'g'),
('Latte', 'ml'),
('Lattuga', 'g'),
('Lenticchie cotte', 'g'),
('Lievito di birra', 'g'),
('Limone', 'pz'),
('Linguine', 'g'),
('Mais', 'g'),
('Manzo macinato', 'g'),
('Marmellata', 'g'),
('Mascarpone', 'g'),
('Melanzane', 'g'),
('Mele', 'g'),
('Merluzzo', 'g'),
('Miele', 'g'),
('Mozzarella', 'g'),
('Noce moscata', 'g'),
('Noci', 'g'),
('Olio di semi', 'ml'),
('Olio extravergine', 'ml'),
('Olive nere', 'g'),
('Origano', 'g'),
('Orzo', 'g'),
('Pane', 'g'),
('Pangrattato', 'g'),
('Panna', 'ml'),
('Paprika', 'g'),
('Parmigiano', 'g'),
('Passata di pomodoro', 'g'),
('Pasta brisée', 'g'),
('Pasta corta', 'g'),
('Pasta sfoglia', 'g'),
('Patate', 'g'),
('Pecorino romano', 'g'),
('Penne', 'g'),
('Pepe nero', 'g'),
('Peperoncino', 'g'),
('Peperoni', 'g'),
('Pere', 'g'),
('Pesto', 'g'),
('Piselli', 'g'),
('Pollo', 'g'),
('Pomodori pelati', 'g'),
('Pomodorini', 'g'),
('Prezzemolo', 'g'),
('Quinoa', 'g'),
('Ricotta', 'g'),
('Riso per risotto', 'g'),
('Rosmarino', 'g'),
('Sale', 'g'),
('Salmone', 'g'),
('Salsiccia', 'g'),
('Salvia', 'g'),
('Savoiardi', 'g'),
('Scalogno', 'g'),
('Sedano', 'g'),
('Spaghetti', 'g'),
('Spinaci', 'g'),
('Tofu', 'g'),
('Tonno sott''olio', 'g'),
('Tortellini', 'g'),
('Uova', 'pz'),
('Vaniglia', 'g'),
('Vino bianco', 'ml'),
('Yogurt bianco', 'g'),
('Zafferano', 'g'),
('Zucca', 'g'),
('Zucchero', 'g'),
('Zucchine', 'g');

-- Ricetta 001/100: Spaghetti alla carbonara
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'carbonara_classica', 'Spaghetti alla carbonara', 'Classico romano con uova, guanciale e pecorino.', 'Rosola il guanciale. Cuoci gli spaghetti. Mescola uova, pecorino e pepe, manteca fuori dal fuoco con poca acqua di cottura.', 4, 25, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'carbonara_classica');
SET @seed_001 = (SELECT id FROM ricette WHERE codice_seed = 'carbonara_classica' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_001, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Spaghetti' AS nome, 320 AS quantita
UNION ALL SELECT 'Uova' AS nome, 4 AS quantita
UNION ALL SELECT 'Guanciale' AS nome, 150 AS quantita
UNION ALL SELECT 'Pecorino romano' AS nome, 60 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_001 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 002/100: Spaghetti al pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'spaghetti_pomodoro', 'Spaghetti al pomodoro', 'Primo semplice con pomodoro e basilico.', 'Rosola l''aglio nell''olio. Aggiungi i pelati e cuoci 15 minuti. Cuoci la pasta, condiscila con il sugo e basilico.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'spaghetti_pomodoro');
SET @seed_002 = (SELECT id FROM ricette WHERE codice_seed = 'spaghetti_pomodoro' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_002, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Spaghetti' AS nome, 320 AS quantita
UNION ALL SELECT 'Pomodori pelati' AS nome, 400 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_002 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 003/100: Spaghetti aglio, olio e peperoncino
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_aglio_olio', 'Spaghetti aglio, olio e peperoncino', 'Un classico veloce della cucina italiana.', 'Cuoci gli spaghetti. Scalda dolcemente aglio, olio e peperoncino, salta la pasta con poca acqua di cottura.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_aglio_olio');
SET @seed_003 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_aglio_olio' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_003, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Spaghetti' AS nome, 320 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 40 AS quantita
UNION ALL SELECT 'Peperoncino' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_003 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 004/100: Bucatini all'amatriciana
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'amatriciana', 'Bucatini all''amatriciana', 'Pasta con guanciale, pomodoro e pecorino.', 'Rosola il guanciale, aggiungi peperoncino e pomodori pelati. Cuoci il sugo 15 minuti e condisci i bucatini, completa con pecorino.', 4, 30, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'amatriciana');
SET @seed_004 = (SELECT id FROM ricette WHERE codice_seed = 'amatriciana' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_004, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Bucatini' AS nome, 320 AS quantita
UNION ALL SELECT 'Guanciale' AS nome, 150 AS quantita
UNION ALL SELECT 'Pomodori pelati' AS nome, 400 AS quantita
UNION ALL SELECT 'Pecorino romano' AS nome, 50 AS quantita
UNION ALL SELECT 'Peperoncino' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 10 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_004 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 005/100: Tonnarelli cacio e pepe
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'cacio_pepe', 'Tonnarelli cacio e pepe', 'Pasta cremosa con pecorino e pepe nero.', 'Cuoci la pasta. Mescola pecorino e pepe con poca acqua di cottura tiepida, manteca lontano dal fuoco.', 4, 20, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'cacio_pepe');
SET @seed_005 = (SELECT id FROM ricette WHERE codice_seed = 'cacio_pepe' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_005, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Spaghetti' AS nome, 320 AS quantita
UNION ALL SELECT 'Pecorino romano' AS nome, 120 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 4 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_005 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 006/100: Pasta al pesto
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_pesto', 'Pasta al pesto', 'Pasta con pesto di basilico e formaggio.', 'Cuoci la pasta e conserva poca acqua. Scola e condisci con pesto, allungando con acqua di cottura se necessario.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_pesto');
SET @seed_006 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_pesto' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_006, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Pesto' AS nome, 120 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 30 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_006 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 007/100: Pasta al tonno e pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_tonno', 'Pasta al tonno e pomodoro', 'Pasta veloce con tonno e passata.', 'Cuoci la pasta. Scalda olio e aglio, aggiungi passata e cuoci 10 minuti, unisci il tonno sgocciolato e condisci.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_tonno');
SET @seed_007 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_tonno' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_007, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Tonno sott''olio' AS nome, 160 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 300 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_007 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 008/100: Pasta con zucchine e parmigiano
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_zucchine', 'Pasta con zucchine e parmigiano', 'Primo delicato con zucchine saltate.', 'Taglia le zucchine e saltale in olio con aglio. Cuoci la pasta, unisci le zucchine e completa con parmigiano.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_zucchine');
SET @seed_008 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_zucchine' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_008, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 400 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 50 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_008 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 009/100: Pasta alla norma
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_melanzane', 'Pasta alla norma', 'Pasta siciliana con melanzane e pomodoro.', 'Taglia e rosola le melanzane. Cuoci la passata con aglio, unisci le melanzane e condisci la pasta.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_melanzane');
SET @seed_009 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_melanzane' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_009, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Melanzane' AS nome, 400 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 350 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 35 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_009 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 010/100: Pasta ricotta e spinaci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_ricotta_spinaci', 'Pasta ricotta e spinaci', 'Pasta cremosa con ricotta e verdure.', 'Cuoci gli spinaci e strizzali. Mescola con ricotta, parmigiano e poca acqua di cottura, condisci la pasta.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_ricotta_spinaci');
SET @seed_010 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_ricotta_spinaci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_010, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Ricotta' AS nome, 250 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 250 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Noce moscata' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_010 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 011/100: Pasta ai funghi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_funghi', 'Pasta ai funghi', 'Pasta con funghi saltati e prezzemolo.', 'Salta i funghi con aglio e olio finché dorati. Cuoci la pasta e amalgama con funghi, prezzemolo e acqua di cottura.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_funghi');
SET @seed_011 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_funghi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_011, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Funghi' AS nome, 350 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_011 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 012/100: Pasta salsiccia e panna
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_salsiccia', 'Pasta salsiccia e panna', 'Pasta ricca con salsiccia rosolata.', 'Rosola la salsiccia sbriciolata e sfuma con poca acqua. Aggiungi panna, cuoci brevemente e condisci la pasta.', 4, 30, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_salsiccia');
SET @seed_012 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_salsiccia' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_012, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Salsiccia' AS nome, 250 AS quantita
UNION ALL SELECT 'Panna' AS nome, 150 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 30 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 10 AS quantita
UNION ALL SELECT 'Sale' AS nome, 3 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_012 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 013/100: Pasta con broccoli e aglio
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_broccoli', 'Pasta con broccoli e aglio', 'Pasta semplice con broccoli e olio.', 'Cuoci i broccoli in acqua salata e schiacciane una parte. Salta con aglio e olio, poi aggiungi la pasta cotta.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_broccoli');
SET @seed_013 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_broccoli' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_013, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Broccoli' AS nome, 400 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Peperoncino' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_013 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 014/100: Pasta ai peperoni
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_peperoni', 'Pasta ai peperoni', 'Pasta con peperoni stufati e basilico.', 'Cuoci lentamente peperoni e cipolla con olio e poca acqua. Frulla una parte, poi condisci la pasta e completa con basilico.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_peperoni');
SET @seed_014 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_peperoni' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_014, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Penne' AS nome, 320 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 400 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_014 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 015/100: Pasta olive e capperi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_olive_capperi', 'Pasta olive e capperi', 'Condimento mediterraneo saporito.', 'Scalda aglio e olio, aggiungi olive, capperi e pomodorini. Cuoci pochi minuti e condisci la pasta.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_olive_capperi');
SET @seed_015 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_olive_capperi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_015, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Linguine' AS nome, 320 AS quantita
UNION ALL SELECT 'Olive nere' AS nome, 80 AS quantita
UNION ALL SELECT 'Capperi' AS nome, 20 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 300 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_015 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 016/100: Linguine con acciughe e pangrattato
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_accughe', 'Linguine con acciughe e pangrattato', 'Pasta saporita con briciole tostate.', 'Tosta il pangrattato in padella. Sciogli le acciughe in olio con aglio, condisci le linguine e termina con pangrattato.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_accughe');
SET @seed_016 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_accughe' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_016, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Linguine' AS nome, 320 AS quantita
UNION ALL SELECT 'Acciughe' AS nome, 40 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 50 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_016 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 017/100: Pasta al salmone e panna
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_salmone', 'Pasta al salmone e panna', 'Pasta cremosa con salmone.', 'Cuoci il salmone a dadini in padella. Aggiungi panna e pepe, cuoci brevemente e condisci la pasta.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_salmone');
SET @seed_017 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_salmone' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_017, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Salmone' AS nome, 300 AS quantita
UNION ALL SELECT 'Panna' AS nome, 150 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 50 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_017 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 018/100: Pasta al gorgonzola
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_gorgonzola', 'Pasta al gorgonzola', 'Salsa cremosa al formaggio.', 'Scalda la panna, sciogli il gorgonzola a fuoco basso e aggiungi pepe. Condisci la pasta appena scolata.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_gorgonzola');
SET @seed_018 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_gorgonzola' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_018, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Penne' AS nome, 320 AS quantita
UNION ALL SELECT 'Gorgonzola' AS nome, 180 AS quantita
UNION ALL SELECT 'Panna' AS nome, 100 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 20 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_018 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 019/100: Pasta con crema di zucca
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_zucca', 'Pasta con crema di zucca', 'Pasta autunnale con zucca e salvia.', 'Cuoci la zucca a cubetti con cipolla e brodo. Frulla, condisci la pasta e aggiungi salvia e parmigiano.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_zucca');
SET @seed_019 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_zucca' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_019, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Zucca' AS nome, 500 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 250 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Salvia' AS nome, 4 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_019 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 020/100: Lasagne alle verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'lasagne_verdure', 'Lasagne alle verdure', 'Lasagne al forno con verdure e besciamella.', 'Salta le verdure a dadini. Alterna sfoglia, verdure, besciamella e parmigiano, cuoci a 180 gradi per circa 35 minuti.', 4, 60, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'lasagne_verdure');
SET @seed_020 = (SELECT id FROM ricette WHERE codice_seed = 'lasagne_verdure' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_020, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta sfoglia' AS nome, 500 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 200 AS quantita
UNION ALL SELECT 'Melanzane' AS nome, 200 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 150 AS quantita
UNION ALL SELECT 'Besciamella' AS nome, 500 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 80 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_020 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 021/100: Risotto allo zafferano
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_zafferano', 'Risotto allo zafferano', 'Risotto cremoso tradizionale.', 'Trita lo scalogno e fallo appassire nel burro. Tosta il riso, sfuma con vino bianco e cuoci aggiungendo brodo, unisci zafferano e manteca.', 4, 30, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_zafferano');
SET @seed_021 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_zafferano' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_021, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Scalogno' AS nome, 60 AS quantita
UNION ALL SELECT 'Burro' AS nome, 50 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Vino bianco' AS nome, 100 AS quantita
UNION ALL SELECT 'Zafferano' AS nome, 1 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 60 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_021 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 022/100: Risotto ai funghi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_funghi', 'Risotto ai funghi', 'Risotto con funghi e prezzemolo.', 'Rosola scalogno e funghi. Tosta il riso, aggiungi brodo poco alla volta e manteca con parmigiano e burro.', 4, 35, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_funghi');
SET @seed_022 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_funghi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_022, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Funghi' AS nome, 350 AS quantita
UNION ALL SELECT 'Scalogno' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Vino bianco' AS nome, 80 AS quantita
UNION ALL SELECT 'Burro' AS nome, 40 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 60 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 6 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_022 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 023/100: Risotto alla zucca
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_zucca', 'Risotto alla zucca', 'Risotto morbido con zucca.', 'Cuoci la zucca a dadini con cipolla. Tosta il riso, aggiungi brodo gradualmente e manteca con burro e parmigiano.', 4, 35, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_zucca');
SET @seed_023 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_zucca' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_023, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Zucca' AS nome, 400 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Burro' AS nome, 40 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 60 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_023 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 024/100: Risotto al radicchio
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_radicchio', 'Risotto al radicchio', 'Risotto dal gusto leggermente amarognolo.', 'Stufa il radicchio con cipolla. Tosta il riso, sfuma con vino e cuoci con brodo, manteca con parmigiano.', 4, 35, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_radicchio');
SET @seed_024 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_radicchio' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_024, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Vino bianco' AS nome, 100 AS quantita
UNION ALL SELECT 'Burro' AS nome, 40 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 60 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_024 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 025/100: Risotto ai piselli
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_piselli', 'Risotto ai piselli', 'Risotto delicato con piselli.', 'Fai appassire la cipolla, tosta il riso e aggiungi brodo. A metà cottura unisci i piselli, manteca con parmigiano.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_piselli');
SET @seed_025 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_piselli' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_025, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Piselli' AS nome, 250 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Burro' AS nome, 35 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 50 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_025 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 026/100: Risotto ai gamberi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'risotto_gamberi', 'Risotto ai gamberi', 'Risotto di mare con gamberi.', 'Rosola i gamberi per pochi minuti e mettili da parte. Cuoci il riso con brodo e vino, aggiungi i gamberi alla fine.', 4, 35, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'risotto_gamberi');
SET @seed_026 = (SELECT id FROM ricette WHERE codice_seed = 'risotto_gamberi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_026, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Riso per risotto' AS nome, 320 AS quantita
UNION ALL SELECT 'Gamberi' AS nome, 300 AS quantita
UNION ALL SELECT 'Scalogno' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 900 AS quantita
UNION ALL SELECT 'Vino bianco' AS nome, 100 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_026 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 027/100: Gnocchi al pomodoro e basilico
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'gnocchi_pomodoro', 'Gnocchi al pomodoro e basilico', 'Gnocchi con salsa semplice.', 'Cuoci la passata con aglio e olio per 15 minuti. Lessa gli gnocchi e condiscili con salsa e basilico.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'gnocchi_pomodoro');
SET @seed_027 = (SELECT id FROM ricette WHERE codice_seed = 'gnocchi_pomodoro' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_027, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Gnocchi di patate' AS nome, 800 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 350 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_027 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 028/100: Gnocchi al gorgonzola
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'gnocchi_gorgonzola', 'Gnocchi al gorgonzola', 'Gnocchi con crema al formaggio.', 'Sciogli gorgonzola e panna a fuoco basso. Cuoci gli gnocchi e condiscili con la salsa e pepe.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'gnocchi_gorgonzola');
SET @seed_028 = (SELECT id FROM ricette WHERE codice_seed = 'gnocchi_gorgonzola' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_028, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Gnocchi di patate' AS nome, 800 AS quantita
UNION ALL SELECT 'Gorgonzola' AS nome, 160 AS quantita
UNION ALL SELECT 'Panna' AS nome, 120 AS quantita
UNION ALL SELECT 'Noci' AS nome, 40 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_028 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 029/100: Tortellini in brodo
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'tortellini_brodo', 'Tortellini in brodo', 'Piatto caldo tradizionale.', 'Porta il brodo a bollore, cuoci i tortellini seguendo la confezione e servi caldo con parmigiano.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'tortellini_brodo');
SET @seed_029 = (SELECT id FROM ricette WHERE codice_seed = 'tortellini_brodo' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_029, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Tortellini' AS nome, 400 AS quantita
UNION ALL SELECT 'Brodo di carne' AS nome, 1200 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_029 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 030/100: Pasta al forno
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_forno', 'Pasta al forno', 'Pasta gratinata con pomodoro e mozzarella.', 'Cuoci la pasta al dente e condiscila con passata. Trasferisci in teglia con mozzarella e parmigiano, gratina a 190 gradi per 15 minuti.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_forno');
SET @seed_030 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_forno' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_030, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 350 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 400 AS quantita
UNION ALL SELECT 'Mozzarella' AS nome, 250 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 60 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_030 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 031/100: Pasta gratinata alla besciamella
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_besciamella', 'Pasta gratinata alla besciamella', 'Pasta al forno con besciamella e formaggio.', 'Cuoci la pasta al dente, mescola con besciamella e parmigiano e gratina in forno a 190 gradi fino a doratura.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_besciamella');
SET @seed_031 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_besciamella' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_031, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Besciamella' AS nome, 350 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 70 AS quantita
UNION ALL SELECT 'Burro' AS nome, 20 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 30 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_031 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 032/100: Pasta con feta e pomodorini
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_feta_pomodori', 'Pasta con feta e pomodorini', 'Pasta al forno con pomodori e feta.', 'Metti pomodorini e feta in teglia con olio e origano. Cuoci a 200 gradi per 25 minuti, schiaccia la feta e mescola con la pasta.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_feta_pomodori');
SET @seed_032 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_feta_pomodori' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_032, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Feta' AS nome, 200 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 400 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_032 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 033/100: Pasta panna e piselli
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_panna_piselli', 'Pasta panna e piselli', 'Pasta cremosa con piselli.', 'Cuoci la cipolla in poco olio, aggiungi i piselli e un goccio d''acqua. Unisci panna e condisci la pasta.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_panna_piselli');
SET @seed_033 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_panna_piselli' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_033, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta corta' AS nome, 320 AS quantita
UNION ALL SELECT 'Piselli' AS nome, 250 AS quantita
UNION ALL SELECT 'Panna' AS nome, 150 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 30 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_033 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 034/100: Pasta primavera
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_primavera', 'Pasta primavera', 'Pasta con un misto di verdure.', 'Taglia le verdure a dadini e saltale in olio finché tenere. Cuoci la pasta e unisci le verdure con basilico.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_primavera');
SET @seed_034 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_primavera' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_034, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Penne' AS nome, 320 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 180 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 150 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Piselli' AS nome, 100 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_034 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 035/100: Couscous alle verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'couscous_verdure', 'Couscous alle verdure', 'Couscous con verdure saltate.', 'Prepara il couscous con acqua calda secondo confezione. Salta zucchine, peperoni e carote, unisci e condisci con limone e olio.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'couscous_verdure');
SET @seed_035 = (SELECT id FROM ricette WHERE codice_seed = 'couscous_verdure' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_035, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Couscous' AS nome, 300 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 200 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 150 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_035 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 036/100: Insalata di quinoa e verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'insalata_quinoa', 'Insalata di quinoa e verdure', 'Insalata fresca e nutriente.', 'Sciacqua e cuoci la quinoa. Lasciala raffreddare e mescola con cetriolo, pomodorini, avocado e limone.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'insalata_quinoa');
SET @seed_036 = (SELECT id FROM ricette WHERE codice_seed = 'insalata_quinoa' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_036, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Quinoa' AS nome, 280 AS quantita
UNION ALL SELECT 'Cetriolo' AS nome, 200 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 250 AS quantita
UNION ALL SELECT 'Avocado' AS nome, 1 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_036 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 037/100: Insalata d'orzo alle verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'orzo_verdure', 'Insalata d''orzo alle verdure', 'Orzo freddo con verdure e olive.', 'Cuoci l''orzo, raffreddalo e mescola con pomodorini, cetriolo, olive e prezzemolo, condisci con olio e limone.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'orzo_verdure');
SET @seed_037 = (SELECT id FROM ricette WHERE codice_seed = 'orzo_verdure' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_037, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Orzo' AS nome, 280 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 250 AS quantita
UNION ALL SELECT 'Cetriolo' AS nome, 150 AS quantita
UNION ALL SELECT 'Olive nere' AS nome, 60 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_037 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 038/100: Frittata agli spinaci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'frittata_spinaci', 'Frittata agli spinaci', 'Frittata morbida con verdure.', 'Cuoci e strizza gli spinaci. Sbatti le uova con parmigiano, unisci gli spinaci e cuoci in padella su entrambi i lati.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'frittata_spinaci');
SET @seed_038 = (SELECT id FROM ricette WHERE codice_seed = 'frittata_spinaci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_038, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Uova' AS nome, 6 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 250 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_038 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 039/100: Frittata di zucchine
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'frittata_zucchine', 'Frittata di zucchine', 'Frittata semplice per pranzo o cena.', 'Affetta le zucchine e saltale in padella. Versa le uova sbattute con parmigiano e cuoci a fuoco basso fino a rassodare.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'frittata_zucchine');
SET @seed_039 = (SELECT id FROM ricette WHERE codice_seed = 'frittata_zucchine' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_039, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Uova' AS nome, 6 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 300 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 40 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_039 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 040/100: Polpette al sugo
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'polpette_manzo', 'Polpette al sugo', 'Polpette di manzo cotte in salsa di pomodoro.', 'Mescola manzo, uovo, pangrattato e parmigiano. Forma polpette, rosolale e cuocile nella passata per circa 20 minuti.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'polpette_manzo');
SET @seed_040 = (SELECT id FROM ricette WHERE codice_seed = 'polpette_manzo' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_040, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Manzo macinato' AS nome, 500 AS quantita
UNION ALL SELECT 'Uova' AS nome, 1 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 60 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 50 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 500 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_040 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 041/100: Hamburger di manzo
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'hamburger_manzo', 'Hamburger di manzo', 'Hamburger fatti in casa in padella.', 'Forma quattro hamburger con la carne, condisci e cuoci in padella ben calda fino al grado di cottura desiderato.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'hamburger_manzo');
SET @seed_041 = (SELECT id FROM ricette WHERE codice_seed = 'hamburger_manzo' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_041, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Manzo macinato' AS nome, 500 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 10 AS quantita
UNION ALL SELECT 'Pane' AS nome, 240 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_041 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 042/100: Pollo al limone
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pollo_limone', 'Pollo al limone', 'Bocconcini di pollo con salsa al limone.', 'Taglia il pollo a bocconcini e rosolalo. Aggiungi succo di limone, poca acqua e cuoci fino a completa cottura.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pollo_limone');
SET @seed_042 = (SELECT id FROM ricette WHERE codice_seed = 'pollo_limone' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_042, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pollo' AS nome, 600 AS quantita
UNION ALL SELECT 'Limone' AS nome, 2 AS quantita
UNION ALL SELECT 'Farina' AS nome, 30 AS quantita
UNION ALL SELECT 'Burro' AS nome, 25 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 10 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_042 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 043/100: Pollo con peperoni
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pollo_peperoni', 'Pollo con peperoni', 'Pollo in padella con peperoni stufati.', 'Rosola il pollo a pezzi, aggiungi cipolla e peperoni. Copri e cuoci finché il pollo è cotto e le verdure morbide.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pollo_peperoni');
SET @seed_043 = (SELECT id FROM ricette WHERE codice_seed = 'pollo_peperoni' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_043, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pollo' AS nome, 600 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 400 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 100 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 150 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_043 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 044/100: Pollo al rosmarino
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pollo_rosmarino', 'Pollo al rosmarino', 'Pollo arrosto profumato alle erbe.', 'Condisci il pollo con olio, rosmarino, sale e pepe. Cuoci in forno a 200 gradi finché ben cotto, girando a metà.', 4, 50, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pollo_rosmarino');
SET @seed_044 = (SELECT id FROM ricette WHERE codice_seed = 'pollo_rosmarino' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_044, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pollo' AS nome, 800 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 5 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 6 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_044 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 045/100: Pollo cremoso ai funghi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pollo_panna_funghi', 'Pollo cremoso ai funghi', 'Pollo con funghi e panna.', 'Rosola il pollo a strisce e mettilo da parte. Cuoci i funghi con cipolla, aggiungi panna e rimetti il pollo fino a cottura completa.', 4, 35, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pollo_panna_funghi');
SET @seed_045 = (SELECT id FROM ricette WHERE codice_seed = 'pollo_panna_funghi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_045, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pollo' AS nome, 600 AS quantita
UNION ALL SELECT 'Funghi' AS nome, 300 AS quantita
UNION ALL SELECT 'Panna' AS nome, 180 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_045 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 046/100: Salsiccia e patate al forno
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'salsiccia_patate', 'Salsiccia e patate al forno', 'Secondo rustico con patate dorate.', 'Taglia le patate a spicchi, condisci con olio e rosmarino e aggiungi la salsiccia. Cuoci in forno a 200 gradi fino a doratura e completa cottura.', 4, 50, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'salsiccia_patate');
SET @seed_046 = (SELECT id FROM ricette WHERE codice_seed = 'salsiccia_patate' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_046, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Salsiccia' AS nome, 500 AS quantita
UNION ALL SELECT 'Patate' AS nome, 700 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 5 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_046 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 047/100: Merluzzo al pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'merluzzo_pomodoro', 'Merluzzo al pomodoro', 'Filetti di merluzzo con salsa mediterranea.', 'Cuoci aglio e pomodorini in olio. Aggiungi il merluzzo, copri e cuoci delicatamente finché il pesce è cotto.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'merluzzo_pomodoro');
SET @seed_047 = (SELECT id FROM ricette WHERE codice_seed = 'merluzzo_pomodoro' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_047, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Merluzzo' AS nome, 600 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 300 AS quantita
UNION ALL SELECT 'Olive nere' AS nome, 50 AS quantita
UNION ALL SELECT 'Capperi' AS nome, 15 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_047 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 048/100: Salmone al forno al limone
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'salmone_forno', 'Salmone al forno al limone', 'Filetti di salmone con limone ed erbe.', 'Disponi il salmone in teglia, condisci con limone, olio, sale e pepe. Cuoci a 190 gradi finché raggiunge una cottura sicura.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'salmone_forno');
SET @seed_048 = (SELECT id FROM ricette WHERE codice_seed = 'salmone_forno' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_048, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Salmone' AS nome, 600 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_048 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 049/100: Gamberi all'aglio e prezzemolo
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'gamberi_aglio', 'Gamberi all''aglio e prezzemolo', 'Gamberi saltati velocemente in padella.', 'Scalda l''olio con aglio, aggiungi i gamberi e cuoci finché diventano opachi e ben cotti. Completa con prezzemolo e limone.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'gamberi_aglio');
SET @seed_049 = (SELECT id FROM ricette WHERE codice_seed = 'gamberi_aglio' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_049, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Gamberi' AS nome, 500 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 10 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_049 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 050/100: Polpette di lenticchie
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'polpette_lenticchie', 'Polpette di lenticchie', 'Polpette vegetariane cotte al forno.', 'Schiaccia le lenticchie e mescola con uovo, pangrattato, carota e spezie. Forma polpette e cuoci a 190 gradi per 20-25 minuti.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'polpette_lenticchie');
SET @seed_050 = (SELECT id FROM ricette WHERE codice_seed = 'polpette_lenticchie' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_050, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Lenticchie cotte' AS nome, 400 AS quantita
UNION ALL SELECT 'Uova' AS nome, 1 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 80 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 50 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 2 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_050 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 051/100: Ceci al pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'ceci_rosso', 'Ceci al pomodoro', 'Ceci stufati in salsa di pomodoro.', 'Rosola cipolla e aglio, aggiungi passata e ceci scolati. Cuoci 15 minuti e completa con olio e prezzemolo.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'ceci_rosso');
SET @seed_051 = (SELECT id FROM ricette WHERE codice_seed = 'ceci_rosso' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_051, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Ceci cotti' AS nome, 500 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 300 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_051 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 052/100: Hummus di ceci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'hummus_ceci', 'Hummus di ceci', 'Crema di ceci con limone e olio.', 'Frulla ceci, succo di limone, aglio, olio e poca acqua fino a ottenere una crema liscia. Regola sale e pepe.', 4, 10, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'hummus_ceci');
SET @seed_052 = (SELECT id FROM ricette WHERE codice_seed = 'hummus_ceci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_052, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Ceci cotti' AS nome, 400 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 35 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_052 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 053/100: Zuppa di lenticchie
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'zuppa_lenticchie', 'Zuppa di lenticchie', 'Zuppa casalinga con verdure.', 'Soffriggi cipolla, carota e sedano. Aggiungi lenticchie cotte e brodo, cuoci 20 minuti e regola il condimento.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'zuppa_lenticchie');
SET @seed_053 = (SELECT id FROM ricette WHERE codice_seed = 'zuppa_lenticchie' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_053, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Lenticchie cotte' AS nome, 500 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Sedano' AS nome, 80 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 800 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 3 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_053 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 054/100: Minestra di cannellini
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'minestra_fagioli', 'Minestra di cannellini', 'Zuppa morbida di fagioli e verdure.', 'Rosola aglio e rosmarino, aggiungi cannellini e brodo. Cuoci 15 minuti, schiaccia una parte dei fagioli e servi con olio.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'minestra_fagioli');
SET @seed_054 = (SELECT id FROM ricette WHERE codice_seed = 'minestra_fagioli' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_054, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Fagioli cannellini' AS nome, 500 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 700 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 3 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Pane' AS nome, 200 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_054 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 055/100: Vellutata di zucca
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'vellutata_zucca', 'Vellutata di zucca', 'Crema liscia di zucca e cipolla.', 'Cuoci zucca e cipolla nel brodo finché morbide. Frulla, aggiungi un poco di olio e servi calda.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'vellutata_zucca');
SET @seed_055 = (SELECT id FROM ricette WHERE codice_seed = 'vellutata_zucca' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_055, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Zucca' AS nome, 700 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 700 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Noce moscata' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_055 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 056/100: Vellutata di cavolfiore
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'vellutata_cavolfiore', 'Vellutata di cavolfiore', 'Crema delicata di cavolfiore.', 'Cuoci cavolfiore e patata nel brodo finché teneri. Frulla e completa con olio, pepe e noce moscata.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'vellutata_cavolfiore');
SET @seed_056 = (SELECT id FROM ricette WHERE codice_seed = 'vellutata_cavolfiore' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_056, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Cavolfiore' AS nome, 600 AS quantita
UNION ALL SELECT 'Patate' AS nome, 200 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 700 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Noce moscata' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_056 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 057/100: Minestrone di verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'minestrone', 'Minestrone di verdure', 'Zuppa di verdure di stagione.', 'Taglia le verdure a dadini. Cuocile nel brodo fino a tenerezza, aggiungendo acqua se necessario, regola sale e olio.', 4, 45, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'minestrone');
SET @seed_057 = (SELECT id FROM ricette WHERE codice_seed = 'minestrone' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_057, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Carota' AS nome, 120 AS quantita
UNION ALL SELECT 'Sedano' AS nome, 100 AS quantita
UNION ALL SELECT 'Patate' AS nome, 250 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 200 AS quantita
UNION ALL SELECT 'Piselli' AS nome, 150 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 1000 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_057 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 058/100: Insalata caprese
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'insalata_caprese', 'Insalata caprese', 'Pomodoro, mozzarella e basilico.', 'Affetta pomodori e mozzarella, alternali sul piatto e condisci con olio, sale e basilico.', 4, 10, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'insalata_caprese');
SET @seed_058 = (SELECT id FROM ricette WHERE codice_seed = 'insalata_caprese' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_058, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pomodorini' AS nome, 400 AS quantita
UNION ALL SELECT 'Mozzarella' AS nome, 300 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 8 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 3 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_058 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 059/100: Insalata greca
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'insalata_greca', 'Insalata greca', 'Insalata fresca con feta e olive.', 'Taglia cetriolo, pomodori e peperone. Aggiungi feta e olive, condisci con olio e origano.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'insalata_greca');
SET @seed_059 = (SELECT id FROM ricette WHERE codice_seed = 'insalata_greca' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_059, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Cetriolo' AS nome, 250 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 300 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 150 AS quantita
UNION ALL SELECT 'Feta' AS nome, 180 AS quantita
UNION ALL SELECT 'Olive nere' AS nome, 60 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_059 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 060/100: Insalata di tonno e cannellini
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'insalata_tonno', 'Insalata di tonno e cannellini', 'Insalata completa con tonno e fagioli.', 'Scola tonno e fagioli, unisci cipolla affettata e prezzemolo. Condisci con olio e limone.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'insalata_tonno');
SET @seed_060 = (SELECT id FROM ricette WHERE codice_seed = 'insalata_tonno' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_060, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Tonno sott''olio' AS nome, 160 AS quantita
UNION ALL SELECT 'Fagioli cannellini' AS nome, 400 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_060 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 061/100: Insalata di avocado e mais
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'insalata_avocado', 'Insalata di avocado e mais', 'Insalata fresca con avocado e mais.', 'Taglia avocado e cetriolo, aggiungi mais e lattuga. Condisci con limone, olio e sale poco prima di servire.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'insalata_avocado');
SET @seed_061 = (SELECT id FROM ricette WHERE codice_seed = 'insalata_avocado' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_061, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Avocado' AS nome, 2 AS quantita
UNION ALL SELECT 'Mais' AS nome, 200 AS quantita
UNION ALL SELECT 'Cetriolo' AS nome, 150 AS quantita
UNION ALL SELECT 'Lattuga' AS nome, 150 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_061 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 062/100: Bruschette al pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'bruschette_pomodoro', 'Bruschette al pomodoro', 'Pane tostato con pomodoro e basilico.', 'Tosta il pane. Condisci i pomodori a dadini con olio, basilico e sale, poi distribuiscili sulle fette.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'bruschette_pomodoro');
SET @seed_062 = (SELECT id FROM ricette WHERE codice_seed = 'bruschette_pomodoro' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_062, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pane' AS nome, 300 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 300 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 8 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 3 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_062 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 063/100: Torta salata ricotta e spinaci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'torta_salata_spinaci', 'Torta salata ricotta e spinaci', 'Torta rustica con ricotta e spinaci.', 'Cuoci e strizza gli spinaci, mescolali con ricotta e uova. Stendi la pasta brisée, farcisci e cuoci a 180 gradi per 35 minuti.', 4, 55, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'torta_salata_spinaci');
SET @seed_063 = (SELECT id FROM ricette WHERE codice_seed = 'torta_salata_spinaci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_063, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pasta brisée' AS nome, 250 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 300 AS quantita
UNION ALL SELECT 'Ricotta' AS nome, 250 AS quantita
UNION ALL SELECT 'Uova' AS nome, 2 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Noce moscata' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_063 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 064/100: Focaccia semplice
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'focaccia_rapida', 'Focaccia semplice', 'Focaccia casalinga con olio e rosmarino.', 'Sciogli il lievito in acqua, unisci farina, sale e olio. Impasta, lascia lievitare fino al raddoppio, stendi e cuoci a 220 gradi.', 4, 120, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'focaccia_rapida');
SET @seed_064 = (SELECT id FROM ricette WHERE codice_seed = 'focaccia_rapida' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_064, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Farina' AS nome, 500 AS quantita
UNION ALL SELECT 'Acqua' AS nome, 300 AS quantita
UNION ALL SELECT 'Lievito di birra' AS nome, 7 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 35 AS quantita
UNION ALL SELECT 'Sale' AS nome, 10 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_064 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 065/100: Crêpes salate alla ricotta
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'crepes_ricotta', 'Crêpes salate alla ricotta', 'Crêpes ripiene di ricotta e spinaci.', 'Sbatti uova, farina e latte fino a ottenere una pastella. Cuoci crêpes sottili, farcisci con ricotta e spinaci e scalda in padella.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'crepes_ricotta');
SET @seed_065 = (SELECT id FROM ricette WHERE codice_seed = 'crepes_ricotta' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_065, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Uova' AS nome, 3 AS quantita
UNION ALL SELECT 'Farina' AS nome, 150 AS quantita
UNION ALL SELECT 'Latte' AS nome, 300 AS quantita
UNION ALL SELECT 'Ricotta' AS nome, 250 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 200 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 30 AS quantita
UNION ALL SELECT 'Burro' AS nome, 15 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_065 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 066/100: Frittelle di mais
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'frittelle_mais', 'Frittelle di mais', 'Frittelle dorate con mais e uova.', 'Mescola mais, uova, farina e poco latte. Forma frittelle e cuocile in padella con poco olio fino a doratura.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'frittelle_mais');
SET @seed_066 = (SELECT id FROM ricette WHERE codice_seed = 'frittelle_mais' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_066, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Mais' AS nome, 250 AS quantita
UNION ALL SELECT 'Uova' AS nome, 2 AS quantita
UNION ALL SELECT 'Farina' AS nome, 100 AS quantita
UNION ALL SELECT 'Latte' AS nome, 80 AS quantita
UNION ALL SELECT 'Olio di semi' AS nome, 25 AS quantita
UNION ALL SELECT 'Sale' AS nome, 3 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_066 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 067/100: Tofu saltato con verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'tofu_verdure', 'Tofu saltato con verdure', 'Piatto vegetariano con tofu e ortaggi.', 'Asciuga e taglia il tofu a cubetti. Rosolalo, aggiungi zucchine e peperoni a listarelle e cuoci finché teneri.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'tofu_verdure');
SET @seed_067 = (SELECT id FROM ricette WHERE codice_seed = 'tofu_verdure' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_067, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Tofu' AS nome, 400 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 200 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 200 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Olio di semi' AS nome, 20 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 2 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_067 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 068/100: Melanzane al forno
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'melanzane_forno', 'Melanzane al forno', 'Melanzane gratinate con pomodoro e parmigiano.', 'Affetta le melanzane, condisci con passata, olio e parmigiano. Cuoci a 190 gradi per circa 30 minuti.', 4, 45, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'melanzane_forno');
SET @seed_068 = (SELECT id FROM ricette WHERE codice_seed = 'melanzane_forno' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_068, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Melanzane' AS nome, 600 AS quantita
UNION ALL SELECT 'Passata di pomodoro' AS nome, 300 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 70 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_068 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 069/100: Zucchine gratinate
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'zucchine_gratinate', 'Zucchine gratinate', 'Zucchine al forno con pangrattato.', 'Taglia le zucchine a metà, condisci con olio, sale e pangrattato. Cuoci a 200 gradi fino a doratura e tenerezza.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'zucchine_gratinate');
SET @seed_069 = (SELECT id FROM ricette WHERE codice_seed = 'zucchine_gratinate' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_069, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Zucchine' AS nome, 600 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 60 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 40 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_069 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 070/100: Patate al forno al rosmarino
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'patate_rosmarino', 'Patate al forno al rosmarino', 'Contorno di patate croccanti.', 'Taglia le patate a spicchi, asciugale e condisci con olio, rosmarino e sale. Cuoci a 200 gradi girandole a metà.', 4, 45, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'patate_rosmarino');
SET @seed_070 = (SELECT id FROM ricette WHERE codice_seed = 'patate_rosmarino' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_070, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Patate' AS nome, 800 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 5 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_070 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 071/100: Verdure stufate mediterranee
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'ratatouille', 'Verdure stufate mediterranee', 'Melanzane, zucchine e peperoni stufati.', 'Taglia le verdure a cubetti. Cuoci cipolla e aglio in olio, aggiungi le verdure e stufa con pomodoro finché morbide.', 4, 40, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'ratatouille');
SET @seed_071 = (SELECT id FROM ricette WHERE codice_seed = 'ratatouille' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_071, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Melanzane' AS nome, 250 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 250 AS quantita
UNION ALL SELECT 'Peperoni' AS nome, 200 AS quantita
UNION ALL SELECT 'Pomodori pelati' AS nome, 300 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Origano' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_071 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 072/100: Cavolfiore speziato al forno
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'cavolfiore_speziato', 'Cavolfiore speziato al forno', 'Cavolfiore arrosto con paprika.', 'Dividi il cavolfiore in cimette, condisci con olio, paprika e sale. Cuoci a 200 gradi finché dorato e tenero.', 4, 35, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'cavolfiore_speziato');
SET @seed_072 = (SELECT id FROM ricette WHERE codice_seed = 'cavolfiore_speziato' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_072, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Cavolfiore' AS nome, 700 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 4 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_072 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 073/100: Broccoli con pangrattato
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'broccoli_pangrattato', 'Broccoli con pangrattato', 'Broccoli saltati con briciole croccanti.', 'Cuoci i broccoli al vapore. Tosta il pangrattato con olio e aglio e usalo per completare i broccoli.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'broccoli_pangrattato');
SET @seed_073 = (SELECT id FROM ricette WHERE codice_seed = 'broccoli_pangrattato' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_073, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Broccoli' AS nome, 500 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 50 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Peperoncino' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_073 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 074/100: Insalata di cannellini e cipolla
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'fagioli_insalata', 'Insalata di cannellini e cipolla', 'Contorno fresco di fagioli.', 'Scola e sciacqua i cannellini. Unisci cipolla affettata e prezzemolo, condisci con olio, limone e pepe.', 4, 10, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'fagioli_insalata');
SET @seed_074 = (SELECT id FROM ricette WHERE codice_seed = 'fagioli_insalata' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_074, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Fagioli cannellini' AS nome, 400 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Prezzemolo' AS nome, 8 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_074 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 075/100: Crostata alla marmellata
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'crostata_marmellata', 'Crostata alla marmellata', 'Dolce casalingo di pasta frolla.', 'Lavora farina, burro, zucchero e uovo. Riposa l''impasto, stendilo in teglia, farcisci con marmellata e cuoci a 180 gradi per 35 minuti.', 8, 60, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'crostata_marmellata');
SET @seed_075 = (SELECT id FROM ricette WHERE codice_seed = 'crostata_marmellata' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_075, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Farina' AS nome, 300 AS quantita
UNION ALL SELECT 'Burro' AS nome, 150 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 120 AS quantita
UNION ALL SELECT 'Uova' AS nome, 1 AS quantita
UNION ALL SELECT 'Marmellata' AS nome, 300 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_075 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 076/100: Tiramisù classico
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'tiramisu', 'Tiramisù classico', 'Dolce al cucchiaio con caffè e mascarpone.', 'Monta i tuorli con zucchero e incorpora mascarpone. Inzuppa rapidamente i savoiardi nel caffè, alterna strati di crema e biscotti e lascia raffreddare. Usa uova pastorizzate se il dolce non viene cotto.', 8, 30, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'tiramisu');
SET @seed_076 = (SELECT id FROM ricette WHERE codice_seed = 'tiramisu' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_076, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Mascarpone' AS nome, 500 AS quantita
UNION ALL SELECT 'Uova' AS nome, 4 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 100 AS quantita
UNION ALL SELECT 'Savoiardi' AS nome, 300 AS quantita
UNION ALL SELECT 'Caffè' AS nome, 300 AS quantita
UNION ALL SELECT 'Cacao amaro' AS nome, 20 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_076 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 077/100: Mousse al cioccolato
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'mousse_cioccolato', 'Mousse al cioccolato', 'Mousse intensa al cioccolato fondente.', 'Sciogli il cioccolato a bagnomaria e lascialo intiepidire. Incorpora delicatamente panna montata e fai rassodare in frigorifero.', 6, 20, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'mousse_cioccolato');
SET @seed_077 = (SELECT id FROM ricette WHERE codice_seed = 'mousse_cioccolato' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_077, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Cioccolato fondente' AS nome, 200 AS quantita
UNION ALL SELECT 'Panna' AS nome, 250 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 30 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_077 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 078/100: Torta di mele
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'torta_mele', 'Torta di mele', 'Torta morbida con mele e cannella.', 'Sbatti uova e zucchero, incorpora farina e latte. Aggiungi mele a fettine e cannella, versa in teglia e cuoci a 180 gradi per 40 minuti.', 8, 60, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'torta_mele');
SET @seed_078 = (SELECT id FROM ricette WHERE codice_seed = 'torta_mele' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_078, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Mele' AS nome, 400 AS quantita
UNION ALL SELECT 'Farina' AS nome, 250 AS quantita
UNION ALL SELECT 'Uova' AS nome, 3 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 150 AS quantita
UNION ALL SELECT 'Latte' AS nome, 120 AS quantita
UNION ALL SELECT 'Burro' AS nome, 80 AS quantita
UNION ALL SELECT 'Cannella' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_078 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 079/100: Coppa yogurt e banana
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'banana_yogurt', 'Coppa yogurt e banana', 'Dessert rapido con yogurt e miele.', 'Affetta le banane e disponile con lo yogurt. Completa con miele e una spolverata di cannella.', 4, 10, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'banana_yogurt');
SET @seed_079 = (SELECT id FROM ricette WHERE codice_seed = 'banana_yogurt' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_079, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Yogurt bianco' AS nome, 400 AS quantita
UNION ALL SELECT 'Banane' AS nome, 2 AS quantita
UNION ALL SELECT 'Miele' AS nome, 30 AS quantita
UNION ALL SELECT 'Cannella' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_079 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 080/100: Pere al cioccolato
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pere_cioccolato', 'Pere al cioccolato', 'Pere cotte con salsa di cioccolato.', 'Taglia le pere a metà e cuocile in poca acqua finché tenere. Sciogli il cioccolato a bagnomaria e versalo sopra le pere.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pere_cioccolato');
SET @seed_080 = (SELECT id FROM ricette WHERE codice_seed = 'pere_cioccolato' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_080, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pere' AS nome, 4 AS quantita
UNION ALL SELECT 'Cioccolato fondente' AS nome, 100 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 20 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_080 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 081/100: Fragole con crema al mascarpone
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'fragole_mascarpone', 'Fragole con crema al mascarpone', 'Fragole fresche con crema dolce.', 'Lava e taglia le fragole. Mescola mascarpone, poco zucchero e vaniglia, poi servi con le fragole.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'fragole_mascarpone');
SET @seed_081 = (SELECT id FROM ricette WHERE codice_seed = 'fragole_mascarpone' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_081, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Fragole' AS nome, 400 AS quantita
UNION ALL SELECT 'Mascarpone' AS nome, 200 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 30 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_081 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 082/100: Biscotti al cacao
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'biscotti_cacao', 'Biscotti al cacao', 'Biscotti friabili al cacao.', 'Mescola farina, cacao, zucchero, burro e uovo. Forma biscotti e cuoci a 180 gradi per 12-15 minuti.', 20, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'biscotti_cacao');
SET @seed_082 = (SELECT id FROM ricette WHERE codice_seed = 'biscotti_cacao' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_082, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Farina' AS nome, 250 AS quantita
UNION ALL SELECT 'Cacao amaro' AS nome, 30 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 100 AS quantita
UNION ALL SELECT 'Burro' AS nome, 100 AS quantita
UNION ALL SELECT 'Uova' AS nome, 1 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_082 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 083/100: Pancake alla banana
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pancake_banane', 'Pancake alla banana', 'Pancake morbidi per colazione.', 'Schiaccia le banane e mescola con uova, farina e latte. Versa piccole porzioni in padella antiaderente e cuoci da entrambi i lati.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pancake_banane');
SET @seed_083 = (SELECT id FROM ricette WHERE codice_seed = 'pancake_banane' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_083, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Banane' AS nome, 2 AS quantita
UNION ALL SELECT 'Uova' AS nome, 2 AS quantita
UNION ALL SELECT 'Farina' AS nome, 150 AS quantita
UNION ALL SELECT 'Latte' AS nome, 120 AS quantita
UNION ALL SELECT 'Olio di semi' AS nome, 10 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_083 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 084/100: Mele cotte alla cannella
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'mele_cannella', 'Mele cotte alla cannella', 'Dessert semplice di mele al forno.', 'Taglia le mele a spicchi, condisci con cannella, miele e poca acqua. Cuoci in forno a 180 gradi finché morbide.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'mele_cannella');
SET @seed_084 = (SELECT id FROM ricette WHERE codice_seed = 'mele_cannella' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_084, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Mele' AS nome, 500 AS quantita
UNION ALL SELECT 'Cannella' AS nome, 3 AS quantita
UNION ALL SELECT 'Miele' AS nome, 25 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_084 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 085/100: Budino al cacao
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'budino_cacao', 'Budino al cacao', 'Budino casalingo al cacao e latte.', 'Mescola cacao, zucchero e farina con poco latte freddo. Aggiungi il restante latte e cuoci mescolando finché addensa, fai raffreddare.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'budino_cacao');
SET @seed_085 = (SELECT id FROM ricette WHERE codice_seed = 'budino_cacao' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_085, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Latte' AS nome, 500 AS quantita
UNION ALL SELECT 'Cacao amaro' AS nome, 35 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 70 AS quantita
UNION ALL SELECT 'Farina' AS nome, 30 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_085 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 086/100: Crumble di mele
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'crumble_mele', 'Crumble di mele', 'Mele morbide con copertura croccante.', 'Disponi le mele a cubetti in una teglia. Sbriciola farina, burro e zucchero, distribuisci sopra e cuoci a 180 gradi per 30 minuti.', 6, 45, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'crumble_mele');
SET @seed_086 = (SELECT id FROM ricette WHERE codice_seed = 'crumble_mele' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_086, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Mele' AS nome, 500 AS quantita
UNION ALL SELECT 'Farina' AS nome, 150 AS quantita
UNION ALL SELECT 'Burro' AS nome, 100 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 100 AS quantita
UNION ALL SELECT 'Cannella' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_086 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 087/100: Cioccolata calda
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'cioccolata_calda', 'Cioccolata calda', 'Bevanda densa al cacao.', 'Mescola cacao, zucchero e amido o farina con poco latte freddo. Aggiungi il latte restante e scalda mescolando fino alla consistenza desiderata.', 4, 15, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'cioccolata_calda');
SET @seed_087 = (SELECT id FROM ricette WHERE codice_seed = 'cioccolata_calda' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_087, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Latte' AS nome, 800 AS quantita
UNION ALL SELECT 'Cacao amaro' AS nome, 40 AS quantita
UNION ALL SELECT 'Zucchero' AS nome, 50 AS quantita
UNION ALL SELECT 'Cioccolato fondente' AS nome, 50 AS quantita
UNION ALL SELECT 'Vaniglia' AS nome, 1 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_087 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 088/100: Quinoa con broccoli e limone
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'quinoa_broccoli', 'Quinoa con broccoli e limone', 'Piatto vegetariano con cereali e verdure.', 'Cuoci la quinoa e i broccoli separatamente. Unisci con olio, succo di limone e pepe, servi tiepido.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'quinoa_broccoli');
SET @seed_088 = (SELECT id FROM ricette WHERE codice_seed = 'quinoa_broccoli' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_088, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Quinoa' AS nome, 280 AS quantita
UNION ALL SELECT 'Broccoli' AS nome, 350 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_088 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 089/100: Couscous con ceci e verdure
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'couscous_ ceci', 'Couscous con ceci e verdure', 'Couscous con ceci e verdure speziate.', 'Prepara il couscous con acqua calda. Salta carota e zucchine, aggiungi ceci e paprika, unisci al couscous con olio e limone.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'couscous_ ceci');
SET @seed_089 = (SELECT id FROM ricette WHERE codice_seed = 'couscous_ ceci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_089, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Couscous' AS nome, 300 AS quantita
UNION ALL SELECT 'Ceci cotti' AS nome, 300 AS quantita
UNION ALL SELECT 'Carota' AS nome, 100 AS quantita
UNION ALL SELECT 'Zucchine' AS nome, 150 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 3 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_089 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 090/100: Tofu alla paprika con patate
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'tofu_paprika', 'Tofu alla paprika con patate', 'Tofu speziato con contorno di patate.', 'Taglia tofu e patate a cubetti. Condisci con olio e paprika, arrostisci le patate e rosola il tofu finché dorato.', 4, 40, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'tofu_paprika');
SET @seed_090 = (SELECT id FROM ricette WHERE codice_seed = 'tofu_paprika' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_090, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Tofu' AS nome, 400 AS quantita
UNION ALL SELECT 'Patate' AS nome, 500 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 4 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_090 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 091/100: Zuppa di pomodoro
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'zuppa_pomodoro', 'Zuppa di pomodoro', 'Zuppa calda di pomodoro e pane.', 'Cuoci cipolla e aglio in olio, aggiungi pomodori pelati e brodo. Cuoci 20 minuti, frulla e servi con pane tostato.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'zuppa_pomodoro');
SET @seed_091 = (SELECT id FROM ricette WHERE codice_seed = 'zuppa_pomodoro' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_091, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pomodori pelati' AS nome, 600 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 500 AS quantita
UNION ALL SELECT 'Pane' AS nome, 200 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_091 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 092/100: Orzotto ai funghi
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'orzo_funghi', 'Orzotto ai funghi', 'Orzo cotto come un risotto con funghi.', 'Rosola funghi e scalogno, aggiungi l''orzo e brodo poco alla volta finché tenero. Manteca con burro e parmigiano.', 4, 40, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'orzo_funghi');
SET @seed_092 = (SELECT id FROM ricette WHERE codice_seed = 'orzo_funghi' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_092, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Orzo' AS nome, 300 AS quantita
UNION ALL SELECT 'Funghi' AS nome, 300 AS quantita
UNION ALL SELECT 'Scalogno' AS nome, 60 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 900 AS quantita
UNION ALL SELECT 'Burro' AS nome, 35 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 50 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 15 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_092 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 093/100: Pasta con pomodorini e basilico
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_pomodorini', 'Pasta con pomodorini e basilico', 'Pasta estiva con pomodorini saltati.', 'Salta i pomodorini con aglio e olio finché rilasciano il succo. Cuoci la pasta, unisci al condimento e aggiungi basilico.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_pomodorini');
SET @seed_093 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_pomodorini' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_093, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Penne' AS nome, 320 AS quantita
UNION ALL SELECT 'Pomodorini' AS nome, 400 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Basilico' AS nome, 8 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 30 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_093 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 094/100: Linguine al limone
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pasta_limone', 'Linguine al limone', 'Pasta fresca con salsa al limone e parmigiano.', 'Cuoci le linguine. Mescola olio, scorza e succo di limone con parmigiano e acqua di cottura, poi manteca la pasta.', 4, 20, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pasta_limone');
SET @seed_094 = (SELECT id FROM ricette WHERE codice_seed = 'pasta_limone' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_094, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Linguine' AS nome, 320 AS quantita
UNION ALL SELECT 'Limone' AS nome, 2 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 70 AS quantita
UNION ALL SELECT 'Burro' AS nome, 25 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_094 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 095/100: Pollo speziato alla paprika
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'pollo_curry', 'Pollo speziato alla paprika', 'Pollo in padella con spezie e yogurt.', 'Rosola il pollo a bocconcini con cipolla e paprika. Aggiungi yogurt e poca acqua, cuoci fino a cottura completa senza far bollire forte.', 4, 30, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'pollo_curry');
SET @seed_095 = (SELECT id FROM ricette WHERE codice_seed = 'pollo_curry' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_095, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Pollo' AS nome, 600 AS quantita
UNION ALL SELECT 'Yogurt bianco' AS nome, 150 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 80 AS quantita
UNION ALL SELECT 'Paprika' AS nome, 4 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_095 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 096/100: Salmone con spinaci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'salmone_spinaci', 'Salmone con spinaci', 'Salmone in padella con spinaci saltati.', 'Cuoci il salmone in padella fino a cottura sicura. Salta gli spinaci con aglio e olio e servi insieme con limone.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'salmone_spinaci');
SET @seed_096 = (SELECT id FROM ricette WHERE codice_seed = 'salmone_spinaci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_096, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Salmone' AS nome, 600 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 300 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 25 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_096 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 097/100: Merluzzo con patate
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'merluzzo_patate', 'Merluzzo con patate', 'Merluzzo al forno con patate.', 'Taglia le patate sottili e cuocile in teglia con olio per 20 minuti. Aggiungi il merluzzo condito e continua finché pesce e patate sono cotti.', 4, 45, 'media'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'merluzzo_patate');
SET @seed_097 = (SELECT id FROM ricette WHERE codice_seed = 'merluzzo_patate' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_097, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Merluzzo' AS nome, 600 AS quantita
UNION ALL SELECT 'Patate' AS nome, 600 AS quantita
UNION ALL SELECT 'Limone' AS nome, 1 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 30 AS quantita
UNION ALL SELECT 'Rosmarino' AS nome, 4 AS quantita
UNION ALL SELECT 'Sale' AS nome, 5 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_097 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 098/100: Zuppa di ceci e spinaci
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'zuppa_ceci_spinaci', 'Zuppa di ceci e spinaci', 'Zuppa semplice di legumi e verdure.', 'Rosola aglio e cipolla, aggiungi ceci e brodo. Cuoci 10 minuti, unisci gli spinaci e cuoci finché appassiscono.', 4, 25, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'zuppa_ceci_spinaci');
SET @seed_098 = (SELECT id FROM ricette WHERE codice_seed = 'zuppa_ceci_spinaci' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_098, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Ceci cotti' AS nome, 400 AS quantita
UNION ALL SELECT 'Spinaci' AS nome, 250 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 60 AS quantita
UNION ALL SELECT 'Aglio' AS nome, 1 AS quantita
UNION ALL SELECT 'Brodo vegetale' AS nome, 700 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_098 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 099/100: Tortino di patate e mozzarella
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'tortino_patate', 'Tortino di patate e mozzarella', 'Tortino al forno filante.', 'Affetta e lessa le patate. Disponile a strati con mozzarella e parmigiano, completa con pangrattato e cuoci a 190 gradi per 25 minuti.', 4, 45, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'tortino_patate');
SET @seed_099 = (SELECT id FROM ricette WHERE codice_seed = 'tortino_patate' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_099, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Patate' AS nome, 700 AS quantita
UNION ALL SELECT 'Mozzarella' AS nome, 250 AS quantita
UNION ALL SELECT 'Parmigiano' AS nome, 50 AS quantita
UNION ALL SELECT 'Pangrattato' AS nome, 40 AS quantita
UNION ALL SELECT 'Burro' AS nome, 20 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_099 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

-- Ricetta 100/100: Frittata di patate
INSERT INTO ricette (utente_id, codice_seed, titolo, descrizione, istruzioni, porzioni, minuti, difficolta)
SELECT NULL, 'frittata_patate', 'Frittata di patate', 'Frittata sostanziosa con patate.', 'Cuoci le patate a dadini in padella con poco olio. Versa le uova sbattute con sale e pepe e cuoci a fuoco basso.', 4, 30, 'facile'
WHERE NOT EXISTS (SELECT 1 FROM ricette WHERE codice_seed = 'frittata_patate');
SET @seed_100 = (SELECT id FROM ricette WHERE codice_seed = 'frittata_patate' LIMIT 1);
INSERT INTO ricetta_ingredienti (ricetta_id, ingrediente_id, quantita)
SELECT @seed_100, i.id, dati.quantita FROM ingredienti i JOIN (
SELECT 'Patate' AS nome, 400 AS quantita
UNION ALL SELECT 'Uova' AS nome, 6 AS quantita
UNION ALL SELECT 'Cipolla' AS nome, 50 AS quantita
UNION ALL SELECT 'Olio extravergine' AS nome, 20 AS quantita
UNION ALL SELECT 'Sale' AS nome, 4 AS quantita
UNION ALL SELECT 'Pepe nero' AS nome, 2 AS quantita
) AS dati ON dati.nome = i.nome
WHERE @seed_100 IS NOT NULL
ON DUPLICATE KEY UPDATE quantita = VALUES(quantita);

COMMIT;
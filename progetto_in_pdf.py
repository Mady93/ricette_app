#!/usr/bin/env python3
"""
progetto_in_pdf.py - Converte un intero progetto in UN SOLO file PDF.

Cosa fa:
  * percorre la cartella del progetto con tutte le sottocartelle;
  * esclude tutto cio' che e' nel .gitignore (letto con le stesse regole di Git,
    compresi i "!eccezioni" come !.env.example) e le cartelle inutili (.git, .venv, ...);
  * non include MAI file con segreti (.env, .env.*, *.pem, *.key) anche se mancano dal .gitignore;
  * per ogni file di testo (.py, .sql, .html, .css, .js, .md, ...) stampa il percorso e il
    contenuto senza numeri di riga;
  * i file binari (immagini, font, ...) o troppo grandi compaiono nell'indice, marcati come omessi;
  * in apertura: struttura ad albero + indice cliccabile con i numeri di pagina;
    nel lettore PDF trovi anche i segnalibri per cartella/file.

Installazione (una volta sola, anche dentro il tuo venv):
    pip install reportlab pathspec

Uso (dalla cartella principale del progetto):
    python progetto_in_pdf.py
    python progetto_in_pdf.py . -o ricette_app.pdf
    python progetto_in_pdf.py C:\\percorso\\ricette_app --max-kb 2000
    python progetto_in_pdf.py --escludi "*.csv" --escludi "docs/"

Opzioni:
    cartella            cartella del progetto (default: quella corrente)
    -o, --output        nome del PDF (default: <nome-cartella>_codice_completo.pdf)
    --max-kb N          salta i file di testo piu' grandi di N KB (default 1024)
    --escludi PATTERN   pattern in stile .gitignore da escludere in piu' (ripetibile)
    --font-size N       dimensione del carattere (default 7.8)
    --font FILE.ttf     font monospazio TrueType da usare (di solito si trova da solo)
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import pathspec
    from reportlab.lib.colors import Color, black
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
except ImportError:
    sys.exit("Mancano delle librerie. Installale con:\n    pip install reportlab pathspec")

# ----------------------------------------------------------------------------- configurazione
CARTELLE_ESCLUSE = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", "htmlcov",
}
FILE_ESCLUSI = {".DS_Store", "Thumbs.db", ".coverage"}
ESTENSIONI_BINARIE = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".svgz", ".tif", ".tiff",
    ".pdf", ".zip", ".gz", ".tar", ".7z", ".rar", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".mp4", ".wav", ".mov", ".avi", ".exe", ".dll", ".so", ".pyd", ".dylib",
    ".db", ".sqlite", ".sqlite3", ".pyc", ".pyo", ".class", ".jar", ".bin", ".dat",
}

NERO = black
GRIGIO = Color(0.45, 0.45, 0.45)
GRIGIO_CHIARO = Color(0.90, 0.91, 0.93)
VIOLA = Color(0.35, 0.22, 0.65)


# ----------------------------------------------------------------------------- raccolta file
def e_segreto(nome: str) -> bool:
    """Rete di sicurezza: questi file non finiscono mai nel PDF."""
    if nome == ".env" or (nome.startswith(".env.") and nome != ".env.example"):
        return True
    return nome.lower().endswith((".pem", ".key"))


def carica_regole(radice: Path, extra):
    righe = []
    gitignore = radice / ".gitignore"
    if gitignore.is_file():
        righe += gitignore.read_text(encoding="utf-8", errors="replace").splitlines()
    else:
        print("Attenzione: .gitignore non trovato, uso solo le esclusioni di base.")
    righe += list(extra)
    try:
        return pathspec.GitIgnoreSpec.from_lines(righe)
    except AttributeError:
        return pathspec.PathSpec.from_lines("gitwildmatch", righe)


class Voce:
    """Un file del progetto con il suo stato."""
    def __init__(self, rel: str, assoluto: Path):
        self.rel = rel
        self.assoluto = assoluto
        self.stato = "ok"
        self.righe = []

    @property
    def omesso(self) -> bool:
        return self.stato not in ("ok", "vuoto")


def leggi_testo(voce: Voce, max_byte: int) -> None:
    p = voce.assoluto
    try:
        dimensione = p.stat().st_size
        if p.suffix.lower() in ESTENSIONI_BINARIE:
            voce.stato = "binario"
            return
        if dimensione > max_byte:
            voce.stato = "troppo grande"
            return
        dati = p.read_bytes()
    except OSError:
        voce.stato = "illeggibile"
        return
    if b"\0" in dati[:8192]:
        voce.stato = "binario"
        return
    if not dati.strip():
        voce.stato = "vuoto"
        return
    for codifica in ("utf-8-sig", "cp1252"):
        try:
            testo = dati.decode(codifica)
            break
        except UnicodeDecodeError:
            continue
    else:
        testo = dati.decode("latin-1")
    voce.righe = testo.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if voce.righe and voce.righe[-1] == "":
        voce.righe.pop()


def raccogli(radice: Path, regole, pdf_uscita: Path, max_byte: int):
    voci, segreti = [], []

    def visita(cartella: Path, rel_cartella: str):
        try:
            elementi = sorted(os.scandir(cartella), key=lambda e: e.name.lower())
        except OSError:
            return
        for e in elementi:
            if e.is_file(follow_symlinks=False):
                rel = f"{rel_cartella}{e.name}"
                if e.name in FILE_ESCLUSI or regole.match_file(rel):
                    continue
                if Path(e.path).resolve() in (pdf_uscita, Path(__file__).resolve()):
                    continue
                if e_segreto(e.name):
                    segreti.append(rel)
                    continue
                v = Voce(rel, Path(e.path))
                leggi_testo(v, max_byte)
                voci.append(v)
        for e in elementi:
            if e.is_dir(follow_symlinks=False):
                if e.name in CARTELLE_ESCLUSE or regole.match_file(f"{rel_cartella}{e.name}/"):
                    continue
                visita(Path(e.path), f"{rel_cartella}{e.name}/")

    visita(radice, "")
    return voci, segreti


# ----------------------------------------------------------------------------- font
def trova_font(percorso_utente):
    windir = os.environ.get("WINDIR", r"C:\Windows")
    candidati = [percorso_utente] if percorso_utente else []
    candidati += [
        os.path.join(windir, "Fonts", "consola.ttf"),
        os.path.join(windir, "Fonts", "cour.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/Library/Fonts/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ]
    for c in candidati:
        if c and os.path.isfile(c):
            try:
                font = TTFont("Mono", c)
                pdfmetrics.registerFont(font)
                glifi = set(font.face.charToGlyph)
                return "Mono", (lambda ch, g=glifi: ord(ch) in g)
            except Exception:
                continue
    print("Nota: nessun font TrueType trovato, uso Courier (i caratteri speciali diventano '?').")

    def in_cp1252(ch):
        try:
            ch.encode("cp1252")
            return True
        except UnicodeEncodeError:
            return False
    return "Courier", in_cp1252


class Pulitore:
    """Rende il testo sicuro per il font scelto: tab, caratteri di controllo, glifi mancanti."""
    def __init__(self, supportato):
        self.supportato = supportato
        self.cache = {}

    def __call__(self, testo: str) -> str:
        testo = testo.expandtabs(4)
        out = []
        for ch in testo:
            r = self.cache.get(ch)
            if r is None:
                if ord(ch) < 32 or ord(ch) == 127:
                    r = ""
                elif self.supportato(ch):
                    r = ch
                else:
                    r = "?"
                self.cache[ch] = r
            out.append(r)
        return "".join(out)


# ----------------------------------------------------------------------------- albero
def costruisci_albero(voci, nome_radice, pulisci, mono_ok):
    radice = {}
    for v in voci:
        parti = v.rel.split("/")
        nodo = radice
        for p in parti[:-1]:
            nodo = nodo.setdefault(p, {})
        nodo[parti[-1]] = v
    if mono_ok("\u251c") and mono_ok("\u2514") and mono_ok("\u2500") and mono_ok("\u2502"):
        T, L, V, S = "\u251c\u2500\u2500 ", "\u2514\u2500\u2500 ", "\u2502   ", "    "
    else:
        T, L, V, S = "|-- ", "`-- ", "|   ", "    "
    righe = [pulisci(nome_radice) + "/"]

    def rec(nodo, prefisso):
        file_ = sorted([(k, x) for k, x in nodo.items() if not isinstance(x, dict)], key=lambda t: t[0].lower())
        dirs = sorted([(k, x) for k, x in nodo.items() if isinstance(x, dict)], key=lambda t: t[0].lower())
        elementi = file_ + dirs
        for i, (nome, x) in enumerate(elementi):
            ultimo = i == len(elementi) - 1
            ramo = L if ultimo else T
            if isinstance(x, dict):
                righe.append(prefisso + ramo + pulisci(nome) + "/")
                rec(x, prefisso + (S if ultimo else V))
            else:
                nota = f"   [omesso: {x.stato}]" if x.omesso else ""
                righe.append(prefisso + ramo + pulisci(nome) + nota)

    rec(radice, "")
    return righe


# ----------------------------------------------------------------------------- impaginazione
class Pagina:
    """Geometria della pagina e conteggi: tutto in 'slot' (una riga di testo = 1 slot)."""
    def __init__(self, dimensione_font, font):
        self.W, self.H = A4
        self.ml, self.mr = 14 * mm, 12 * mm
        self.mt, self.mb = 20 * mm, 16 * mm
        self.fs = dimensione_font
        self.lead = dimensione_font * 1.28
        self.font = font
        self.cw = pdfmetrics.stringWidth("M", font, dimensione_font)
        self.slot_per_pagina = int((self.H - self.mt - self.mb) // self.lead)
        self.colonne = int((self.W - self.ml - self.mr) // self.cw)

    def baseline(self, slot):
        return self.H - self.mt - (slot + 1) * self.lead + (self.lead - self.fs) * 0.55


def spezza(testo, larghezza):
    if len(testo) <= larghezza:
        return [testo]
    return [testo[i:i + larghezza] for i in range(0, len(testo), larghezza)]


def impagina_corpo(voci, pg: Pagina, pulisci):
    """Ritorna (pagine, pagina_iniziale_per_voce). Ogni pagina e' una lista di operazioni."""
    pagine = [[]]
    usati = 0
    inizio = {}

    def nuova_pagina():
        nonlocal usati
        pagine.append([])
        usati = 0

    def aggiungi(op, slot=1):
        nonlocal usati
        if usati + slot > pg.slot_per_pagina:
            nuova_pagina()
        pagine[-1].append(op)
        usati += slot

    for i, v in enumerate(voci):
        if usati > 0 and pg.slot_per_pagina - usati < 6:
            nuova_pagina()
        inizio[i] = len(pagine) - 1
        aggiungi(("hdr", i), 2)
        if v.stato == "vuoto":
            aggiungi(("nota", i, "(file vuoto)"))
        elif v.omesso:
            motivo = {"binario": "file binario", "troppo grande": "file troppo grande",
                      "illeggibile": "file non leggibile"}[v.stato]
            aggiungi(("nota", i, f"[contenuto omesso: {motivo}]"))
        else:
            # Larghezza massima senza numeri di riga
            larghezza = pg.colonne
            for riga in v.righe:
                for pezzo in spezza(pulisci(riga), larghezza):
                    aggiungi(("riga", i, pezzo))
        aggiungi(("vuota", i))

    while len(pagine) > 1 and not pagine[-1]:
        pagine.pop()
    return pagine, inizio


def impagina_inizio(voci, albero, pg: Pagina, info):
    ops = [("titolo", info["titolo"]), ("testo", info["sottotitolo"])]
    for riga in info["statistiche"]:
        ops.append(("testo", riga))
    ops.append(("vuota", None))
    ops.append(("h2", "Struttura del progetto"))
    for r in albero:
        for pezzo in spezza(r, pg.colonne):
            ops.append(("albero", pezzo))
    ops.append(("vuota", None))
    ops.append(("h2", "Indice dei file"))
    for i, v in enumerate(voci):
        ops.append(("indice", i))

    peso = {"titolo": 3, "h2": 2}
    pagine, corrente, usati = [], [], 0
    for op in ops:
        s = peso.get(op[0], 1)
        if usati + s > pg.slot_per_pagina:
            pagine.append(corrente)
            corrente, usati = [], 0
        corrente.append(op)
        usati += s
    pagine.append(corrente)
    return pagine


# ----------------------------------------------------------------------------- disegno
def disegna(percorso_pdf, voci, nome_progetto, pg: Pagina, pulisci, front, corpo, inizio, info):
    n_front = len(front)
    totale = n_front + len(corpo)
    c = canvas.Canvas(str(percorso_pdf), pagesize=A4, pageCompression=1)
    c.setTitle(f"{nome_progetto} codice completo")
    c.setSubject("Esportazione del codice sorgente del progetto")
    c.setCreator("progetto_in_pdf.py")

    def cornice(numero, testo_alto):
        c.setFillColor(GRIGIO)
        c.setFont("Helvetica", 7.5)
        c.drawString(pg.ml, pg.H - 11 * mm, pulisci_h(f"{nome_progetto}   |   {testo_alto}"))
        c.setStrokeColor(GRIGIO_CHIARO)
        c.setLineWidth(0.6)
        c.line(pg.ml, pg.H - 13 * mm, pg.W - pg.mr, pg.H - 13 * mm)
        c.drawRightString(pg.W - pg.mr, 9 * mm, f"Pagina {numero} di {totale}")
        c.drawString(pg.ml, 9 * mm, info["data"])

    def pulisci_h(t):
        return t.encode("latin-1", "replace").decode("latin-1")

    pagina_di_voce = {i: n_front + inizio[i] + 1 for i in inizio}
    cartelle_aperte = []

    # ---- pagine iniziali
    for p_idx, ops in enumerate(front):
        numero = p_idx + 1
        if p_idx == 0:
            c.bookmarkPage("inizio")
            c.addOutlineEntry("Struttura e indice", "inizio", 0)
        cornice(numero, "Struttura e indice")
        slot = 0
        for op in ops:
            tipo = op[0]
            if tipo == "titolo":
                c.setFillColor(VIOLA)
                c.setFont("Helvetica-Bold", 20)
                c.drawString(pg.ml, pg.H - pg.mt - 20, pulisci_h(op[1]))
                slot += 3
            elif tipo == "h2":
                c.setFillColor(VIOLA)
                c.setFont("Helvetica-Bold", 12)
                c.drawString(pg.ml, pg.baseline(slot + 1) + 2, pulisci_h(op[1]))
                slot += 2
            elif tipo == "testo":
                c.setFillColor(NERO)
                c.setFont("Helvetica", 9)
                c.drawString(pg.ml, pg.baseline(slot), pulisci_h(op[1]))
                slot += 1
            elif tipo == "albero":
                c.setFillColor(NERO)
                c.setFont(pg.font, pg.fs)
                c.drawString(pg.ml, pg.baseline(slot), op[1])
                slot += 1
            elif tipo == "indice":
                v = voci[op[1]]
                pagina = str(pagina_di_voce[op[1]])
                nota = " [omesso]" if v.omesso else ""
                nome = pulisci(v.rel) + nota
                spazio = pg.colonne - len(pagina) - 2
                if len(nome) > spazio:
                    nome = "..." + nome[-(spazio - 3):]
                punti = "." * max(2, pg.colonne - len(nome) - len(pagina) - 2)
                c.setFillColor(NERO)
                c.setFont(pg.font, pg.fs)
                c.drawString(pg.ml, pg.baseline(slot), f"{nome} {punti} {pagina}")
                y = pg.baseline(slot)
                c.linkRect("", f"f{op[1]}", (pg.ml, y - 2, pg.W - pg.mr, y + pg.fs), relative=0, thickness=0)
                slot += 1
            else:
                slot += 1
        c.showPage()

    # ---- corpo
    for p_idx, ops in enumerate(corpo):
        numero = n_front + p_idx + 1
        primo_file = next((op[1] for op in ops if op[0] in ("hdr", "riga", "nota", "vuota")), None)
        cornice(numero, voci[primo_file].rel if primo_file is not None else "")
        slot = 0
        for op in ops:
            tipo = op[0]
            if tipo == "hdr":
                i = op[1]
                v = voci[i]
                chiave = f"f{i}"
                c.bookmarkPage(chiave)
                parti = v.rel.split("/")
                cartelle = parti[:-1]
                comune = 0
                while (comune < len(cartelle) and comune < len(cartelle_aperte)
                       and cartelle[comune] == cartelle_aperte[comune]):
                    comune += 1
                del cartelle_aperte[comune:]
                for livello in range(comune, len(cartelle)):
                    c.addOutlineEntry(pulisci_h(cartelle[livello] + "/"), chiave, livello)
                    cartelle_aperte.append(cartelle[livello])
                c.addOutlineEntry(pulisci_h(parti[-1]), chiave, len(cartelle))
                
                y_top = pg.H - pg.mt - slot * pg.lead
                c.setFillColor(GRIGIO_CHIARO)
                c.rect(pg.ml - 2, y_top - 2 * pg.lead + 2, pg.W - pg.ml - pg.mr + 4, 2 * pg.lead - 2, stroke=0, fill=1)
                c.setFillColor(VIOLA)
                c.setFont("Helvetica-Bold", 9.5)
                c.drawString(pg.ml + 2, y_top - pg.lead - 1, pulisci_h(v.rel))
                c.setFillColor(GRIGIO)
                c.setFont("Helvetica", 7.5)
                if v.stato == "ok":
                    dettaglio = f"{len(v.righe)} righe"
                else:
                    dettaglio = v.stato
                c.drawRightString(pg.W - pg.mr - 2, y_top - pg.lead - 1, dettaglio)
                slot += 2
            elif tipo == "riga":
                _, i, testo = op
                y = pg.baseline(slot)
                c.setFillColor(NERO)
                c.setFont(pg.font, pg.fs)
                c.drawString(pg.ml, y, testo)
                slot += 1
            elif tipo == "nota":
                c.setFillColor(GRIGIO)
                c.setFont("Helvetica-Oblique", 8.5)
                c.drawString(pg.ml + 2, pg.baseline(slot), pulisci_h(op[2]))
                slot += 1
            else:
                slot += 1
        c.showPage()

    c.save()
    return totale


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Converte un intero progetto in un unico PDF (rispetta il .gitignore).")
    ap.add_argument("cartella", nargs="?", default=".", help="cartella del progetto (default: corrente)")
    ap.add_argument("-o", "--output", help="nome del PDF di uscita")
    ap.add_argument("--max-kb", type=int, default=1024, help="salta i file di testo piu' grandi di N KB")
    ap.add_argument("--escludi", action="append", default=[], metavar="PATTERN",
                    help="pattern in stile .gitignore da escludere in piu' (ripetibile)")
    ap.add_argument("--font-size", type=float, default=7.8)
    ap.add_argument("--font", help="percorso di un font monospazio .ttf")
    args = ap.parse_args()

    radice = Path(args.cartella).resolve()
    if not radice.is_dir():
        sys.exit(f"Cartella non trovata: {radice}")
    nome = radice.name or "progetto"
    uscita = Path(args.output) if args.output else Path.cwd() / f"{nome}_codice_completo.pdf"
    uscita = uscita.resolve()

    print(f"Leggo il progetto: {radice}")
    regole = carica_regole(radice, args.escludi)
    voci, segreti = raccogli(radice, regole, uscita, args.max_kb * 1024)
    if not voci:
        sys.exit("Nessun file da includere: controlla la cartella e il .gitignore.")

    font, supportato = trova_font(args.font)
    pulisci = Pulitore(supportato)
    pg = Pagina(args.font_size, font)

    corpo, inizio = impagina_corpo(voci, pg, pulisci)
    righe_totali = sum(len(v.righe) for v in voci if v.stato == "ok")
    n_omessi = sum(1 for v in voci if v.omesso)
    ora = datetime.now().strftime("%d/%m/%Y %H:%M")
    info = {
        "titolo": nome,
        "sottotitolo": f"Codice completo del progetto - generato il {ora}",
        "statistiche": [
            f"File: {len(voci)}   |   Righe di testo: {righe_totali}   |   File omessi (binari/grandi): {n_omessi}",
            "Esclusi: .gitignore, cartelle di sistema/cache e file con segreti (.env, chiavi).",
        ],
        "data": ora,
    }
    albero = costruisci_albero(voci, nome, pulisci, supportato)
    front = impagina_inizio(voci, albero, pg, info)
    totale = disegna(uscita, voci, nome, pg, pulisci, front, corpo, inizio, info)

    print(f"\nPDF creato: {uscita}")
    print(f"  {len(voci)} file ({n_omessi} omessi: binari/troppo grandi), {righe_totali} righe, {totale} pagine")
    if segreti:
        print("  Esclusi per sicurezza (segreti): " + ", ".join(segreti))
    omessi = [v.rel + f" ({v.stato})" for v in voci if v.omesso]
    if omessi:
        print("  Contenuto omesso: " + ", ".join(omessi[:15]) + (" ..." if len(omessi) > 15 else ""))


if __name__ == "__main__":
    main()
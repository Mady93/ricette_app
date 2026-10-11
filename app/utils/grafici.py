"""Grafici della home, disegnati con matplotlib.

Il grafico è un'immagine PNG incorporata nella pagina come data URI: così non servono
script né stili inline (la CSP del sito li blocca) e non serve una rotta in più.
Si usa Figure e non pyplot perché pyplot tiene uno stato globale e non è sicuro
quando Flask serve più richieste insieme.
"""
import base64
from functools import lru_cache
from io import BytesIO
from typing import Tuple

from matplotlib.figure import Figure

INK = "#17153b"
INK_MUTE = "#6f6e8c"
PINK_DEEP = "#c51162"
PINK_MID = "#e0508a"
PINK_LIGHT = "#f7b6cf"
TRACK = "#fbe6ef"
VERDE = "#1faa6b"         # difficoltà facile
AMBRA = "#f2a516"         # difficoltà media


def _in_data_uri(fig: Figure) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.05)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def _accorcia(testo: str, n: int = 24) -> str:
    return testo if len(testo) <= n else testo[: n - 1] + "…"

def _colore_copertura(p: int) -> str:
    """Più ingredienti hai già, più la barra è verde."""
    if p >= 70:
        return VERDE
    if p >= 40:
        return AMBRA
    return PINK_DEEP

@lru_cache(maxsize=64)   # stessi dati = stessa immagine, senza ridisegnarla
def copertura_ricette(voci: Tuple[Tuple[str, int], ...]) -> str:
    """Barre orizzontali: per ogni ricetta, che percentuale degli ingredienti hai già."""
    n = len(voci)
    fig = Figure(figsize=(5.4, 0.55 * n + 0.2), dpi=200)
    ax = fig.add_subplot(111)

    nomi = [_accorcia(t) for t, _ in voci][::-1]
    perc = [p for _, p in voci][::-1]

    ax.barh(nomi, [100] * n, color=TRACK, height=0.46)
    ax.barh(nomi, perc, color=[_colore_copertura(p) for p in perc], height=0.46)
    for y, p in enumerate(perc):
        ax.text(103, y, f"{p}%", va="center", ha="left", fontsize=9, fontweight="bold", color=INK)

    ax.set_xlim(0, 118)
    ax.tick_params(axis="y", length=0, labelsize=9.5, labelcolor=INK, pad=6)
    ax.set_xticks([])
    for lato in ax.spines.values():
        lato.set_visible(False)
    return _in_data_uri(fig)


@lru_cache(maxsize=64)
def ricette_per_difficolta(facile: int, media: int, difficile: int) -> str:
    """Barre orizzontali: quante ricette ci sono per ogni livello di difficoltà."""
    livelli = [
        ("Facile", "●○○", facile, VERDE),
        ("Media", "●●○", media, AMBRA),
        ("Difficile", "●●●", difficile, PINK_DEEP),
    ]
    totale = facile + media + difficile
    massimo = max(facile, media, difficile, 1)

    fig = Figure(figsize=(5.4, 2.5), dpi=200)
    ax = fig.add_subplot(111)

    for riga, (nome, pallini, n, colore) in enumerate(livelli):
        y = len(livelli) - 1 - riga                      # "Facile" in alto
        ax.barh(y, massimo, color=TRACK, height=0.42)    # sfondo chiaro
        ax.barh(y, n, color=colore, height=0.42)         # valore reale
        perc = round(100 * n / totale) if totale else 0
        ax.text(-0.04 * massimo, y + 0.06, nome, ha="right", va="center",
                fontsize=10.5, fontweight="bold", color=INK)
        ax.text(-0.04 * massimo, y - 0.2, pallini, ha="right", va="center",
                fontsize=8.5, color=colore)
        ax.text(massimo * 1.04, y, f"{n}  ({perc}%)", ha="left", va="center",
                fontsize=10, fontweight="bold", color=INK)

    ax.set_xlim(0, massimo * 1.4)
    ax.set_ylim(-0.6, len(livelli) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([])
    for lato in ax.spines.values():
        lato.set_visible(False)
    ax.set_title(f"{totale} ricette, dalla più semplice alla più impegnativa",
                 loc="left", fontsize=9.5, color=INK_MUTE, pad=8)
    return _in_data_uri(fig)
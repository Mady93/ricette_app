def qta(valore):
    """320.0 -> '320', 2.5 -> '2,5' (formato italiano)."""
    if valore is None:
        return ""
    v = float(valore)
    testo = str(int(v)) if v == int(v) else f"{v:.2f}".rstrip("0").rstrip(".")
    return testo.replace(".", ",")

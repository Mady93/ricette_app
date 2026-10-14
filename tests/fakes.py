"""Repository finti in memoria: i service si testano senza MySQL."""
from itertools import count

from app.models.admin import IngredienteRiepilogo, RicettaRiepilogo, UtenteRiepilogo
from app.models.dispensa import Suggerimento, VoceDispensa
from app.models.ingrediente import Ingrediente
from app.models.ricetta import RicettaSintesi, RigaRicetta


class FakeUtenteRepository:
    def __init__(self):
        self.d, self._n = {}, count(1)
        self.ricette = None          # collegato dalla fixture: serve a contare e a "scollegare" le ricette

    def find_by_id(self, i): return self.d.get(i)
    def find_by_identificativo(self, x):
        return next((u for u in self.d.values() if u.username == x or u.email == x.lower()), None)
    def exists_by_username(self, x): return any(u.username == x for u in self.d.values())
    def exists_by_email(self, x): return any(u.email == x for u in self.d.values())
    def save(self, u):
        u.id = next(self._n)
        self.d[u.id] = u
        return u.id

    # ---- area admin ----
    def find_all_con_ricette(self):
        return [UtenteRiepilogo(u.id, u.username, u.email, u.ruolo, u.creato_il,
                                sum(1 for r in self._ricette() if r.utente_id == u.id))
                for u in sorted(self.d.values(), key=lambda u: u.username)]
    def conta(self): return len(self.d)
    def conta_admin(self): return sum(1 for u in self.d.values() if u.ruolo == "admin")
    def update_ruolo(self, i, ruolo): self.d[i].ruolo = ruolo
    def delete(self, i):
        self.d.pop(i)
        for r in self._ricette():                      # come ON DELETE SET NULL
            if r.utente_id == i:
                r.utente_id = None

    def _ricette(self):
        return self.ricette.d.values() if self.ricette else []


class FakeIngredienteRepository:
    def __init__(self):
        self.d, self._n = {}, count(1)
        self.ricette = self.dispensa = None   # collegati dalla fixture: servono a contare gli utilizzi

    def find_all(self): return sorted(self.d.values(), key=lambda i: i.nome)
    def find_ids_esistenti(self, ids): return {i for i in ids if i in self.d}
    def exists_by_nome(self, n): return any(i.nome == n for i in self.d.values())
    def save(self, nome, unita):
        i = next(self._n)
        self.d[i] = Ingrediente(i, nome, unita)
        return i

    # ---- area admin ----
    def find_by_id(self, i): return self.d.get(i)
    def utilizzi(self, i):
        n_ricette = sum(1 for righe in (self.ricette.r.values() if self.ricette else [])
                        if any(g == i for g, _ in righe))
        n_dispense = sum(1 for (_, ing) in (self.dispensa.d if self.dispensa else {}) if ing == i)
        return n_ricette, n_dispense
    def find_all_con_utilizzi(self):
        return [IngredienteRiepilogo(x.id, x.nome, x.unita_base, *self.utilizzi(x.id))
                for x in self.find_all()]
    def exists_by_nome_escluso(self, nome, i):
        return any(x.nome == nome and x.id != i for x in self.d.values())
    def update(self, i, nome, unita):
        self.d[i].nome, self.d[i].unita_base = nome, unita
    def delete(self, i):
        self.d.pop(i)
        if self.dispensa:                              # come ON DELETE CASCADE
            for chiave in [k for k in self.dispensa.d if k[1] == i]:
                self.dispensa.d.pop(chiave)
    def conta(self): return len(self.d)
    def conta_inutilizzati(self): return sum(1 for x in self.d.values() if self.utilizzi(x.id)[0] == 0)


class FakeRicettaRepository:
    def __init__(self, ingredienti):
        self.d, self.r, self._n, self.ing = {}, {}, count(1), ingredienti
        self.utenti = None           # collegato dalla fixture: serve a mostrare l'autore

    def _filtra(self, q, d, m):
        return [r for r in self.d.values()
                if (not q or q.lower() in r.titolo.lower())
                and (not d or r.difficolta == d) and (not m or r.minuti <= m)]

    def conta(self, q, d, m): return len(self._filtra(q, d, m))
    def cerca(self, q, d, m, limite, offset):
        tutte = sorted(self._filtra(q, d, m), key=lambda r: -r.id)
        return [RicettaSintesi(r.id, r.titolo, r.descrizione, r.porzioni, r.minuti, r.difficolta)
                for r in tutte][offset:offset + limite]
    def find_by_id(self, i): return self.d.get(i)
    def righe_di(self, i):
        return [RigaRicetta(g, self.ing.d[g].nome, self.ing.d[g].unita_base, q) for g, q in self.r.get(i, [])]
    def save(self, r, righe):
        r.id = next(self._n)
        self.d[r.id] = r
        self.r[r.id] = list(righe)
        return r.id
    def update(self, r, righe):
        r.utente_id = self.d[r.id].utente_id
        self.d[r.id], self.r[r.id] = r, list(righe)
    def delete(self, i):
        self.d.pop(i)
        self.r.pop(i)

    # ---- area admin ----
    def _filtra_admin(self, q, solo_senza_autore):
        return [r for r in self.d.values()
                if (not q or q.lower() in r.titolo.lower())
                and (not solo_senza_autore or r.utente_id is None)]
    def conta_admin(self, q, solo_senza_autore): return len(self._filtra_admin(q, solo_senza_autore))
    def cerca_admin(self, q, solo_senza_autore, limite, offset):
        tutte = sorted(self._filtra_admin(q, solo_senza_autore), key=lambda r: -r.id)
        def autore(r):
            u = self.utenti.d.get(r.utente_id) if (self.utenti and r.utente_id) else None
            return u.username if u else None
        return [RicettaRiepilogo(r.id, r.titolo, autore(r), r.minuti, r.difficolta, None)
                for r in tutte][offset:offset + limite]


class FakeDispensaRepository:
    def __init__(self, ingredienti, ricette):
        self.d, self.ing, self.ric = {}, ingredienti, ricette

    def find_by_utente(self, u):
        return [VoceDispensa(i, self.ing.d[i].nome, self.ing.d[i].unita_base, q)
                for (uu, i), q in self.d.items() if uu == u]
    def upsert(self, u, i, q): self.d[(u, i)] = q
    def delete(self, u, i): self.d.pop((u, i), None)
    def possedute_per_ricetta(self, u, rid):
        return {g: self.d[(u, g)] for g, _ in self.ric.r.get(rid, []) if (u, g) in self.d}
    def suggerimenti(self, u, limite):
        out = []
        for rid, r in self.ric.d.items():
            righe = self.ric.r[rid]
            pos = sum(1 for g, q in righe if self.d.get((u, g), 0) >= q)
            if pos:
                out.append(Suggerimento(rid, r.titolo, r.minuti, r.difficolta, len(righe), pos))
        return sorted(out, key=lambda x: (-x.posseduti / x.totale, x.totale))[:limite]

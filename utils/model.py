from utils.controller import *

class Kino:
    def __init__(self, siec, nazwa, lokalizacja, czy_pobrac_wspolrzedne=True):
        self.siec = siec
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        if czy_pobrac_wspolrzedne:
            self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)
        else:
            self.wspolrzedne = (52.23, 21.00)
        self.marker = None

    def aktualizuj(self, siec, nazwa, lokalizacja):
        self.siec = siec
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)

    def do_slownika(self):
        return {
            "siec": self.siec,
            "nazwa": self.nazwa,
            "lokalizacja": self.lokalizacja,
            "wspolrzedne": self.wspolrzedne
        }

    @classmethod
    def z_slownika(cls, d):
        domyslne_wspolrzedne = (52.23, 21.00)
        lokalizacja = d.get("lokalizacja", "").strip()
        if not lokalizacja:
            print(f"\nBrak lokalizacji dla kina {d.get('nazwa', '')} — przypisano domyślne współrzędne.")
            obiekt = cls(d.get("siec", ""), d.get("nazwa", ""), lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt

        wsp = d.get("wspolrzedne")
        wspolrzedne_z_pliku  = None
        if wsp and isinstance(wsp, (list, tuple)) and len(wsp) == 2:
            try:
                wspolrzedne_z_pliku  = (float(wsp[0]), float(wsp[1]))
            except Exception:
                wspolrzedne_z_pliku  = None

        if wspolrzedne_z_pliku  and wspolrzedne_z_pliku  != domyslne_wspolrzedne:
            obiekt = cls(d["siec"], d["nazwa"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = wspolrzedne_z_pliku
            return obiekt
        elif lokalizacja.strip().lower() == "warszawa":
            obiekt = cls(d["siec"], d["nazwa"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt
        else:
            return cls(d["siec"], d["nazwa"], lokalizacja, czy_pobrac_wspolrzedne=True)


class Seans:
    def __init__(self, tytul, data, godzina_rozpoczecia, czas_trwania, kino):
        self.tytul = tytul
        self.data = data
        self.godzina_rozpoczecia = godzina_rozpoczecia
        self.czas_trwania = czas_trwania
        self.kino = kino
        self.marker = None

    def aktualizuj(self, tytul, data, godzina_rozpoczecia, czas_trwania, kino):
        self.tytul = tytul
        self.data = data
        self.godzina_rozpoczecia = godzina_rozpoczecia
        self.czas_trwania = czas_trwania
        self.kino = kino

    def do_slownika(self):
        return {
            "tytul": self.tytul,
            "data": self.data,
            "godzina_rozpoczecia": self.godzina_rozpoczecia,
            "czas_trwania": self.czas_trwania,
            "kino": self.kino
        }

    @classmethod
    def z_slownika(cls, d):
        if "data" not in d:
            from datetime import datetime
            domyslna_data = datetime.now().strftime("%d.%m.%Y")
            return cls(d["tytul"], domyslna_data, d["godzina_rozpoczecia"], d["czas_trwania"], d["kino"])
        return cls(d["tytul"], d["data"], d["godzina_rozpoczecia"], d["czas_trwania"], d["kino"])


class Pracownik:
    def __init__(self, imie, nazwisko, kino, lokalizacja, czy_pobrac_wspolrzedne=True):
        self.imie = imie
        self.nazwisko = nazwisko
        self.kino = kino
        self.lokalizacja = lokalizacja
        if czy_pobrac_wspolrzedne:
            self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)
        else:
            self.wspolrzedne = (52.23, 21.00)
        self.marker = None

    def aktualizuj(self, imie, nazwisko, kino, lokalizacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.kino = kino
        self.lokalizacja = lokalizacja
        self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)

    def do_slownika(self):
        return {
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "kino": self.kino,
            "lokalizacja": self.lokalizacja,
            "wspolrzedne": self.wspolrzedne
        }

    @classmethod
    def z_slownika(cls, d):
        domyslne_wspolrzedne = (52.23, 21.00)

        lokalizacja = d.get("lokalizacja", "").strip()
        if not lokalizacja:
            print(f"\nBrak lokalizacji dla pracownika {d.get('imie', '')} {d.get('nazwisko', '')} — przypisano domyślne współrzędne.")
            obiekt = cls(d.get("imie", ""), d.get("nazwisko", ""), d.get("kino", ""), lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt

        wsp = d.get("wspolrzedne")
        wspolrzedne_z_pliku  = None
        if wsp and isinstance(wsp, (list, tuple)) and len(wsp) == 2:
            try:
                wspolrzedne_z_pliku  = (float(wsp[0]), float(wsp[1]))
            except Exception:
                wspolrzedne_z_pliku  = None

        lokalizacja_lower = lokalizacja.lower()

        if wspolrzedne_z_pliku  and wspolrzedne_z_pliku  != domyslne_wspolrzedne:
            obiekt = cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = wspolrzedne_z_pliku
            return obiekt
        elif lokalizacja_lower == "warszawa":
            obiekt = cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt
        else:
            return cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=True)


class Klient:
    def __init__(self, imie, nazwisko, kino, lokalizacja, czy_pobrac_wspolrzedne=True):
        self.imie = imie
        self.nazwisko = nazwisko
        self.kino = kino
        self.lokalizacja = lokalizacja
        if czy_pobrac_wspolrzedne:
            self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)
        else:
            self.wspolrzedne = (52.23, 21.00)
        self.marker = None

    def aktualizuj(self, imie, nazwisko, kino, lokalizacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.kino = kino
        self.lokalizacja = lokalizacja
        self.wspolrzedne = pobierz_wspolrzedne(lokalizacja)

    def do_slownika(self):
        return {
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "kino": self.kino,
            "lokalizacja": self.lokalizacja,
            "wspolrzedne": self.wspolrzedne
        }

    @classmethod
    def z_slownika(cls, d):
        domyslne_wspolrzedne = (52.23, 21.00)
        lokalizacja = d.get("lokalizacja", "").strip()
        if not lokalizacja:
            print(f"\nBrak lokalizacji dla klienta {d.get('imie', '')} {d.get('nazwisko', '')} — przypisano domyślne współrzędne.")
            obiekt = cls(d.get("imie", ""), d.get("nazwisko", ""), d.get("kino", ""), lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt

        wsp = d.get("wspolrzedne")
        wspolrzedne_z_pliku  = None
        if wsp and isinstance(wsp, (list, tuple)) and len(wsp) == 2:
            try:
                wspolrzedne_z_pliku  = (float(wsp[0]), float(wsp[1]))
            except Exception:
                wspolrzedne_z_pliku  = None

        if wspolrzedne_z_pliku  and wspolrzedne_z_pliku  != domyslne_wspolrzedne:
            obiekt = cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = wspolrzedne_z_pliku
            return obiekt
        elif lokalizacja.strip().lower() == "warszawa":
            obiekt = cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=False)
            obiekt.wspolrzedne = domyslne_wspolrzedne
            return obiekt
        else:
            return cls(d["imie"], d["nazwisko"], d["kino"], lokalizacja, czy_pobrac_wspolrzedne=True)


kina = []
seanse = []
pracownicy = []
klienci = []


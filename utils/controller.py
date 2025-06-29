import json
import os

from utils import model


def ustaw_folder_danych(katalog_bazowy):
    model.folder_danych = os.path.join(katalog_bazowy, model.folder_nazwa)
    os.makedirs(model.folder_danych, exist_ok=True)
    model.plik_kin = os.path.join(model.folder_danych, "Kina.json")
    model.plik_seansow = os.path.join(model.folder_danych, "Seanse.json")
    model.plik_pracownikow = os.path.join(model.folder_danych, "Pracownicy.json")
    model.plik_klientow = os.path.join(model.folder_danych, "Klienci.json")


def zapisz_dane():
    """ Zapisuje dane kin, pracowników i klientów do plików JSON."""
    with open(model.plik_kin, "w", encoding="utf-8") as f:
        json.dump([kino.do_slownika() for kino in model.kina], f, ensure_ascii=False, indent=4)
    with open(model.plik_seansow, "w", encoding="utf-8") as f:
        json.dump([seans.do_slownika() for seans in model.seanse], f, ensure_ascii=False, indent=4)
    with open(model.plik_pracownikow, "w", encoding="utf-8") as f:
        json.dump([pracownik.do_slownika() for pracownik in model.pracownicy], f, ensure_ascii=False, indent=4)
    with open(model.plik_klientow, "w", encoding="utf-8") as f:
        json.dump([klient.do_slownika() for klient in model.klienci], f, ensure_ascii=False, indent=4)
    print("\nDane zapisane.")


def wczytaj_dane():
    if os.path.exists(model.plik_kin) and os.path.getsize(model.plik_kin) > 0:
        with open(model.plik_kin, "r", encoding="utf-8") as f:
            try:
                lista = json.load(f)
                model.kina = [model.Kino.z_slownika(d) for d in lista]
            except json.decoder.JSONDecodeError:
                model.kina = []
    else:
        model.kina = []

    if os.path.exists(model.plik_seansow) and os.path.getsize(model.plik_seansow) > 0:
        with open(model.plik_seansow, "r", encoding="utf-8") as f:
            try:
                lista = json.load(f)
                model.seanse = [model.Seans.z_slownika(d) for d in lista]
            except json.decoder.JSONDecodeError:
                model.seanse = []
    else:
        model.seanse = []

    if os.path.exists(model.plik_pracownikow) and os.path.getsize(model.plik_pracownikow) > 0:
        with open(model.plik_pracownikow, "r", encoding="utf-8") as f:
            try:
                lista = json.load(f)
                model.pracownicy = [model.Pracownik.z_slownika(d) for d in lista]
            except json.decoder.JSONDecodeError:
                model.pracownicy = []
    else:
        model.pracownicy = []

    if os.path.exists(model.plik_klientow) and os.path.getsize(model.plik_klientow) > 0:
        with open(model.plik_klientow, "r", encoding="utf-8") as f:
            try:
                lista = json.load(f)
                model.klienci = [model.Klient.z_slownika(d) for d in lista]
            except json.decoder.JSONDecodeError:
                model.klienci = []
    else:
        model.klienci = []

    print("\nDane wczytane.")


def sprawdz_format_daty(data):
    try:
        dzien, miesiac, rok = data.split('.')
        if len(dzien) != 2 or len(miesiac) != 2 or len(rok) != 4:
            return False
        dzien = int(dzien)
        miesiac = int(miesiac)
        rok = int(rok)
        return (1 <= dzien <= 31) and (1 <= miesiac <= 12) and (rok >= 1900)
    except (ValueError, AttributeError):
        return False


def sprawdz_format_godziny(godzina):
    try:
        godzina, minuty = godzina.split(':')
        if len(godzina) != 2 or len(minuty) != 2:
            return False
        godzina = int(godzina)
        minuty = int(minuty)
        return 0 <= godzina <= 23 and 0 <= minuty <= 59
    except (ValueError, AttributeError):
        return False


def aktualizuj_wspolrzedne():

    for kino in model.kina:
        nowe_wspolrzedne = model.pobierz_wspolrzedne(kino.lokalizacja)
        if nowe_wspolrzedne != (52.23, 21.00):
            kino.wspolrzedne = nowe_wspolrzedne

    for pracownik in model.pracownicy:
        nowe_wspolrzedne = model.pobierz_wspolrzedne(pracownik.lokalizacja)
        if nowe_wspolrzedne != (52.23, 21.00):
            pracownik.wspolrzedne = nowe_wspolrzedne

    for klient in model.klienci:
        nowe_wspolrzedne = model.pobierz_wspolrzedne(klient.lokalizacja)
        if nowe_wspolrzedne != (52.23, 21.00):
            klient.wspolrzedne = nowe_wspolrzedne

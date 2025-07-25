import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
import ctypes
import tempfile
import os

from utils import model, controller


szczegoly_kina_tekst = "Nie wybrano kina."
szczegoly_pracownika_tekst = "Nie wybrano pracownika."
szczegoly_klienta_tekst = "Nie wybrano klienta."
szczegoly_seansu_tekst = "Nie wybrano seansu."


# -------------------------- FUNKCJE DO OBSŁUGI POŁĄCZENIA Z INTERNETEM -------------------------- #


def wyswietl_brak_internetu():
    root.after(0, lambda: messagebox.showwarning("Brak połączenia z Internetem",
                                                 "Utracono połączenie z Internetem. Proszę połączyć się z siecią, aby korzystać z pełnej funkcjonalności aplikacji"))


def podlaczono_internet():
    root.after(0, lambda: messagebox.showinfo("Połączono z Internetem",
                                              "Internet został ponownie przywrócony. Wszystkie informacje zostały zaktualizowane i odświeżone."))
    root.after(10, wyczysc_mape)
    root.after(10, aktualizuj_wspolrzedne_po_polaczeniu)
    root.after(10, odswiez_mape)


def aktualizuj_wspolrzedne_po_polaczeniu():
    controller.aktualizuj_wspolrzedne()
    globalna_aktualizacja()
    if zakladki.tab(zakladki.select(), "text") == "Mapa":
        odswiez_mape()


# -------------------------- FUNKCJE DO ZARZĄDZANIA KINAMI -------------------------- #


def wyswietl_kino(kino):
    return f"{kino.nazwa} ({kino.siec})"


def odswiez_liste_kin():
    current_selection = lista_kin.curselection()
    lista_kin.delete(0, tk.END)

    filtr = lista_rozwijalna_filtru_kin.get()
    for indeks, kino in enumerate(model.kina):
        if filtr == "Wszystkie" or kino.siec == filtr:
            lista_kin.insert(tk.END, f"{indeks + 1}. {wyswietl_kino(kino)} - {kino.lokalizacja}")

    if current_selection and current_selection[0] < lista_kin.size():
        lista_kin.selection_set(current_selection[0])
        lista_kin.activate(current_selection[0])
        pokaz_szczegoly_kina(None)

#    print("\nFunkcja odswiez_liste_kin: Lista została zaktualizowana.")


def odswiez_filtr_sieci_kin():
    sieci = sorted({kino.siec for kino in model.kina})
    lista_rozwijalna_filtru_kin['values'] = ["Wszystkie"] + sieci
    lista_rozwijalna_filtru_kin.set("Wszystkie")


def pokaz_szczegoly_kina(event=None):
    global szczegoly_kina_tekst
    try:
        indeks = lista_kin.curselection()[0]
        kino = model.kina[indeks]

        liczba_pracownikow = len([p for p in model.pracownicy if p.kino == wyswietl_kino(kino)])
        liczba_klientow = len([k for k in model.klienci if k.kino == wyswietl_kino(kino)])
        liczba_seansow = len([s for s in model.seanse if s.kino == wyswietl_kino(kino)])

        szczegoly = (
            f"Nazwa: {kino.nazwa}\n"
            f"Sieć: {kino.siec}\n"
            f"Lokalizacja: {kino.lokalizacja}\n"
            f"Współrzędne: {kino.wspolrzedne}\n"
            f"Liczba pracowników: {liczba_pracownikow}\n"
            f"Liczba klientów: {liczba_klientow}\n"
            f"Liczba seansów: {liczba_seansow}"
        )

        szczegoly_kina_tekst = szczegoly
        informacje_o_wybranym_kinie.config(text=szczegoly_kina_tekst)
        informacje_o_wybranym_kinie.update_idletasks()
    except (IndexError, AttributeError):
        informacje_o_wybranym_kinie.config(text="Nie wybrano kina.")
        informacje_o_wybranym_kinie.update_idletasks()


def aktualizuj_kino(indeks):
    siec = pole_kino_siec.get()
    nazwa = pole_kino_nazwa.get()
    lokalizacja = pole_kino_lokalizacja.get()

    if siec and nazwa and lokalizacja:
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "warszawa":
            messagebox.showerror("Błąd", "Podano błędną lokalizację, wprowadź prawidłową lokalizację.")
            return

        stara_nazwa = wyswietl_kino(model.kina[indeks])
        model.kina[indeks].aktualizuj(siec, nazwa, lokalizacja)
        nowa_nazwa = wyswietl_kino(model.kina[indeks])

        if stara_nazwa != nowa_nazwa:
            for pracownik in model.pracownicy:
                if pracownik.kino == stara_nazwa:
                    pracownik.kino = nowa_nazwa
            for klient in model.klienci:
                if klient.kino == stara_nazwa:
                    klient.kino = nowa_nazwa
            for seans in model.seanse:
                if seans.kino == stara_nazwa:
                    seans.kino = nowa_nazwa

        globalna_aktualizacja()
        przycisk_dodaj_kina.config(text="Dodaj", command=dodaj_kino)
        pole_kino_siec.delete(0, tk.END)
        pole_kino_nazwa.delete(0, tk.END)
        pole_kino_lokalizacja.delete(0, tk.END)
        if lista_kin.curselection():
            pokaz_szczegoly_kina(None)
        informacje_o_wybranym_kinie.update_idletasks()
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla kina (Sieć, Nazwa, Lokalizacja).")


def edytuj_kino():
    try:
        indeks = lista_kin.curselection()[0]
        wybrane_kino = model.kina[indeks]
        pole_kino_siec.delete(0, tk.END)
        pole_kino_siec.insert(0, wybrane_kino.siec)
        pole_kino_nazwa.delete(0, tk.END)
        pole_kino_nazwa.insert(0, wybrane_kino.nazwa)
        pole_kino_lokalizacja.delete(0, tk.END)
        pole_kino_lokalizacja.insert(0, wybrane_kino.lokalizacja)
        przycisk_dodaj_kina.config(text="Zapisz", command=lambda: aktualizuj_kino(indeks))
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano kina do edycji.")


def usun_kino():
    try:
        indeks = lista_kin.curselection()[0]
        del model.kina[indeks]
        odswiez_liste_kin()
        odswiez_listy_rozwijalne_kin()
        odswiez_filtr_sieci_kin()
        globalna_aktualizacja()
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano kina do usunięcia.")


def dodaj_kino():
    siec = pole_kino_siec.get()
    nazwa = pole_kino_nazwa.get()
    lokalizacja = pole_kino_lokalizacja.get()
    if siec and nazwa and lokalizacja:
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "warszawa":
            messagebox.showerror("Błąd", "Podano błędną lokalizację, wprowadź prawidłową lokalizację.")
            return
        nowe_kino = model.Kino(siec, nazwa, lokalizacja)
        model.kina.append(nowe_kino)
        globalna_aktualizacja()
        pole_kino_siec.delete(0, tk.END)
        pole_kino_nazwa.delete(0, tk.END)
        pole_kino_lokalizacja.delete(0, tk.END)

    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla kina (Sieć, Nazwa, Lokalizacja).")


# -------------------------- FUNKCJE DO ZARZĄDZANIA SEANSAMI -------------------------- #


def odswiez_liste_seansow():
    lista_seansow.delete(0, tk.END)
    wybrane_kino = lista_rozwijalna_seans_kino.get()

    filtrowane_seanse = [s for s in model.seanse if wybrane_kino == "Wszystkie" or s.kino == wybrane_kino]

    for indeks, seans in enumerate(filtrowane_seanse):
        kino_seansu = None
        for k in model.kina:
            if wyswietl_kino(k) == seans.kino:
                kino_seansu = k
                break

        if kino_seansu:
            wpis = f"{indeks + 1}. {seans.tytul} ({seans.godzina_rozpoczecia}, {seans.data}) - {kino_seansu.nazwa} ({kino_seansu.siec})"
        else:
            wpis = f"{indeks + 1}. {seans.tytul} ({seans.godzina_rozpoczecia}, {seans.data}) - {seans.kino}"

        lista_seansow.insert(tk.END, wpis)

#    print("\nFunkcja odswiez_liste_seansow: Lista została zaktualizowana.")


def aktualizuj_seanse_po_zmianie_kina(stara_nazwa, nowa_nazwa):
    for seans in model.seanse:
        if seans.kino == stara_nazwa:
            seans.kino = nowa_nazwa
    globalna_aktualizacja()


def dodaj_seans():
    tytul = pole_seans_tytul.get()
    data = pole_seans_data.get()
    godzina = pole_seans_godzina.get()
    czas_trwania = pole_seans_czas_trwania.get()
    kino_wybrane = lista_rozwijalna_seans_kino.get()

    if tytul and data and godzina and czas_trwania and kino_wybrane and kino_wybrane != "Wybierz kino":
        if not controller.sprawdz_format_daty(data):
            messagebox.showerror("Błąd", "Podaj datę w formacie DD.MM.RRRR (np. 31.12.2023)")
            return

        if not controller.sprawdz_format_godziny(godzina):
            messagebox.showerror("Błąd", "Podaj godzinę w formacie HH:MM (np. 14:30)")
            return

        try:
            czas_trwania = int(czas_trwania)
            if czas_trwania <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Czas trwania seansu musi być liczbą całkowitą większą od 0.")
            return

        nowy_seans = model.Seans(tytul, data, godzina, czas_trwania, kino_wybrane)
        model.seanse.append(nowy_seans)
        globalna_aktualizacja()
        pole_seans_tytul.delete(0, tk.END)
        pole_seans_data.delete(0, tk.END)
        pole_seans_godzina.delete(0, tk.END)
        pole_seans_czas_trwania.delete(0, tk.END)
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla seansu (Tytuł, Data, Godzina, Czas trwania).")


def usun_seans():
    try:
        wybrane_kino = lista_rozwijalna_seans_kino.get()
        filtrowani = [s for s in model.seanse if wybrane_kino == "Wszystkie" or s.kino == wybrane_kino]
        indeks = lista_seansow.curselection()[0]
        seans = filtrowani[indeks]
        model.seanse.remove(seans)
        odswiez_liste_seansow()
        aktualizuj_liste_seansow_na_mapie()
        globalna_aktualizacja()
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano seansu do usunięcia.")


def edytuj_seans():
    try:
        wybrane_kino = lista_rozwijalna_seans_kino.get()
        filtrowani = [s for s in model.seanse if wybrane_kino == "Wszystkie" or s.kino == wybrane_kino]
        indeks = lista_seansow.curselection()[0]
        seans = filtrowani[indeks]

        pole_seans_tytul.delete(0, tk.END)
        pole_seans_tytul.insert(0, seans.tytul)
        pole_seans_data.delete(0, tk.END)
        pole_seans_data.insert(0, seans.data)
        pole_seans_godzina.delete(0, tk.END)
        pole_seans_godzina.insert(0, seans.godzina_rozpoczecia)
        pole_seans_czas_trwania.delete(0, tk.END)
        pole_seans_czas_trwania.insert(0, seans.czas_trwania)
        lista_rozwijalna_seans_kino.set(seans.kino)

        przycisk_dodaj_seans.config(text="Zapisz", command=lambda: aktualizuj_seans(seans))
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano seansu do edycji.")


def aktualizuj_seans(seans):
    tytul = pole_seans_tytul.get()
    data = pole_seans_data.get()
    godzina = pole_seans_godzina.get()
    czas_trwania = pole_seans_czas_trwania.get()
    kino_wybrane = lista_rozwijalna_seans_kino.get()

    if tytul and data and godzina and czas_trwania and kino_wybrane:
        if not controller.sprawdz_format_daty(data):
            messagebox.showerror("Błąd", "Podaj datę w formacie DD.MM.RRRR (np. 31.12.2023)")
            return

        if not controller.sprawdz_format_godziny(godzina):
            messagebox.showerror("Błąd", "Podaj godzinę w formacie HH:MM (np. 14:30)")
            return

        try:
            czas_trwania = int(czas_trwania)
            if czas_trwania <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Czas trwania seansu musi być liczbą całkowitą większą od 0.")
            return

        seans.aktualizuj(tytul, data, godzina, czas_trwania, kino_wybrane)
        pokaz_szczegoly_seansu()
        globalna_aktualizacja()
        przycisk_dodaj_seans.config(text="Dodaj", command=dodaj_seans)
        pole_seans_tytul.delete(0, tk.END)
        pole_seans_data.delete(0, tk.END)
        pole_seans_godzina.delete(0, tk.END)
        pole_seans_czas_trwania.delete(0, tk.END)
        odswiez_liste_seansow()
        if lista_seansow.curselection():
            pokaz_szczegoly_seansu(None)
        informacje_o_wybranym_seansie.update_idletasks()
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla seansu (Tytuł, Data, Godzina, Czas trwania).")
        globalna_aktualizacja()


def pokaz_szczegoly_seansu(event=None):
    global szczegoly_seansu_tekst
    try:
        wybrane_kino = lista_rozwijalna_seans_kino.get()
        filtrowani = [s for s in model.seanse if wybrane_kino == "Wszystkie" or s.kino == wybrane_kino]
        indeks = lista_seansow.curselection()[0]
        seans = filtrowani[indeks]

        kino_seansu = None
        for k in model.kina:
            if wyswietl_kino(k) == seans.kino:
                kino_seansu = k
                break

        podstawowe_szczegoly = (
            f"Tytuł: {seans.tytul}\n"
            f"Data: {seans.data}\n"
            f"Godzina: {seans.godzina_rozpoczecia}\n"
            f"Czas trwania: {seans.czas_trwania} min\n"
            f"Kino: {seans.kino}\n"
        )

        dodatkowe_szczegoly = ""
        if seans.kino != "Wszystkie":
            dodatkowe_szczegoly = (
                f"Lokalizacja kina: {kino_seansu.lokalizacja if kino_seansu else 'Nieznana'}\n"
                f"Sieć kina: {kino_seansu.siec if kino_seansu else 'Wszystkie'}\n"
            )

        szczegoly = podstawowe_szczegoly + dodatkowe_szczegoly

        szczegoly_seansu_tekst = szczegoly
        informacje_o_wybranym_seansie.config(text=szczegoly_seansu_tekst)
    except IndexError:
        informacje_o_wybranym_seansie.config(text="Nie wybrano seansu.")


# -------------------------- FUNKCJE DO ZARZĄDZANIA PRACOWNIKAMI -------------------------- #


def odswiez_liste_pracownikow():
    lista_pracownikow.delete(0, tk.END)
    wybrane_kino = lista_rozwijalna_pracownik_kino.get()

    if wybrane_kino == "Wszystkie" or not wybrane_kino:
        for indeks, pracownik in enumerate(model.pracownicy):
            lista_pracownikow.insert(tk.END, f"{indeks + 1}. {pracownik.imie} {pracownik.nazwisko} - {pracownik.kino}")
    else:
        for indeks, pracownik in enumerate([p for p in model.pracownicy if p.kino == wybrane_kino]):
            lista_pracownikow.insert(tk.END, f"{indeks + 1}. {pracownik.imie} {pracownik.nazwisko} - {pracownik.kino}")

#    print("\nFunkcja odswiez_liste_pracownikow: Lista została zaktualizowana.")


def dodaj_pracownika():
    imie = pole_pracownik_imie.get()
    nazwisko = pole_pracownik_nazwisko.get()
    lokalizacja = pole_pracownik_lokalizacja.get()
    kino_wybrane = lista_rozwijalna_pracownik_kino.get()
    if imie and nazwisko and lokalizacja and kino_wybrane and kino_wybrane != "Wybierz kino":
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "Warszawa":
            messagebox.showerror("Błąd", "Błędna lokalizacja, wprowadź poprawną lokalizację.")
            return
        nowy_pracownik = model.Pracownik(imie, nazwisko, kino_wybrane, lokalizacja)
        model.pracownicy.append(nowy_pracownik)
        globalna_aktualizacja()
        pole_pracownik_imie.delete(0, tk.END)
        pole_pracownik_nazwisko.delete(0, tk.END)
        pole_pracownik_lokalizacja.delete(0, tk.END)
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla pracownika (Imię, Nazwisko, Lokalizacja).")


def usun_pracownika():
    try:
        indeks = lista_pracownikow.curselection()[0]
        wybrane_kino = lista_rozwijalna_pracownik_kino.get()

        if wybrane_kino == "Wszystkie":
            pracownik = model.pracownicy[indeks]
        else:
            pracownik = [p for p in model.pracownicy if p.kino == wybrane_kino][indeks]

        model.pracownicy.remove(pracownik)
        odswiez_liste_pracownikow()
        globalna_aktualizacja()
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano pracownika do usunięcia.")


def edytuj_pracownika():
    try:
        wybrane_kino = lista_rozwijalna_pracownik_kino.get()
        filtrowani = [p for p in model.pracownicy if wybrane_kino == "Wszystkie" or p.kino == wybrane_kino]
        indeks = lista_pracownikow.curselection()[0]
        pracownik = filtrowani[indeks]
        pole_pracownik_imie.delete(0, tk.END)
        pole_pracownik_imie.insert(0, pracownik.imie)
        pole_pracownik_nazwisko.delete(0, tk.END)
        pole_pracownik_nazwisko.insert(0, pracownik.nazwisko)
        pole_pracownik_lokalizacja.delete(0, tk.END)
        pole_pracownik_lokalizacja.insert(0, pracownik.lokalizacja)
        lista_rozwijalna_pracownik_kino.set(pracownik.kino)
        przycisk_dodaj_pracownik.config(text="Zapisz", command=lambda: aktualizuj_pracownika(pracownik))
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano pracownika do edycji.")


def aktualizuj_pracownika(pracownik):
    imie = pole_pracownik_imie.get()
    nazwisko = pole_pracownik_nazwisko.get()
    lokalizacja = pole_pracownik_lokalizacja.get()
    kino_wybrane = lista_rozwijalna_pracownik_kino.get()

    if imie and nazwisko and lokalizacja and kino_wybrane:
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "Warszawa":
            messagebox.showerror("Błąd", "Podano błędną lokalizację, wprowadź prawidłową lokalizację.")
            return

        pracownik.aktualizuj(imie, nazwisko, kino_wybrane, lokalizacja)
        pokaz_szczegoly_pracownika()
        globalna_aktualizacja()
        przycisk_dodaj_pracownik.config(text="Dodaj", command=dodaj_pracownika)
        pole_pracownik_imie.delete(0, tk.END)
        pole_pracownik_nazwisko.delete(0, tk.END)
        pole_pracownik_lokalizacja.delete(0, tk.END)
        odswiez_liste_pracownikow()
        if lista_pracownikow.curselection():
            pokaz_szczegoly_pracownika(None)
        informacje_o_wybranym_pracowniku.update_idletasks()
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla pracownika (Imię, Nazwisko, Lokalizacja).")


def pokaz_szczegoly_pracownika(event=None):
    global szczegoly_pracownika_tekst
    try:
        indeks = lista_pracownikow.curselection()[0]
        pracownik = model.pracownicy[indeks]

        kino_pracownika = None
        for k in model.kina:
            if wyswietl_kino(k) == pracownik.kino:
                kino_pracownika = k
                break

        podstawowe_szczegoly = (
            f"Imię: {pracownik.imie}\n"
            f"Nazwisko: {pracownik.nazwisko}\n"
        )

        if pracownik.kino == "Wszystkie":
            podstawowe_szczegoly += f"Kino: {pracownik.kino}\n"

        dodatkowe_szczegoly = ""
        if pracownik.kino != "Wszystkie":
            dodatkowe_szczegoly = (
                f"Lokalizacja: {pracownik.lokalizacja}\n"
                f"Współrzędne: {pracownik.wspolrzedne}\n"
                f"Kino: {pracownik.kino}\n"
                f"Lokalizacja kina: {kino_pracownika.lokalizacja if kino_pracownika else 'Nieznana'}\n"
            )

        szczegoly = podstawowe_szczegoly + dodatkowe_szczegoly + (
            f"Sieć kina: {kino_pracownika.siec if kino_pracownika else 'Wszystkie'}\n"
        )

        szczegoly_pracownika_tekst = szczegoly
        informacje_o_wybranym_pracowniku.config(text=szczegoly_pracownika_tekst)
    except IndexError:
        informacje_o_wybranym_pracowniku.config(text="Nie wybrano pracownika.")


# -------------------------- ZAKŁADKA KLIENCI -------------------------- #


def odswiez_liste_klientow():
    lista_klientow.delete(0, tk.END)
    wybrane_kino = lista_rozwijalna_klient_kino.get()

    if wybrane_kino == "Wszystkie" or not wybrane_kino:
        for indeks, klient in enumerate(model.klienci):
            lista_klientow.insert(tk.END, f"{indeks + 1}. {klient.imie} {klient.nazwisko} - {klient.kino}")
    else:
        for indeks, klient in enumerate([k for k in model.klienci if k.kino == wybrane_kino]):
            lista_klientow.insert(tk.END, f"{indeks + 1}. {klient.imie} {klient.nazwisko} - {klient.kino}")

#    print("\nFunkcja odswiez_liste_klientow: Lista została zaktualizowana.")


def dodaj_klienta():
    imie = pole_klient_imie.get()
    nazwisko = pole_klient_nazwisko.get()
    lokalizacja = pole_klient_lokalizacja.get()
    kino_wybrane = lista_rozwijalna_klient_kino.get()
    if imie and nazwisko and lokalizacja and kino_wybrane and kino_wybrane != "Wybierz kino":
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "Warszawa":
            messagebox.showerror("Błąd", "Błędna lokalizacja, wprowadź poprawną lokalizację.")
            return
        nowy_klient = model.Klient(imie, nazwisko, kino_wybrane, lokalizacja)
        model.klienci.append(nowy_klient)
        globalna_aktualizacja()
        pole_klient_imie.delete(0, tk.END)
        pole_klient_nazwisko.delete(0, tk.END)
        pole_klient_lokalizacja.delete(0, tk.END)
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla klienta (Imię, Nazwisko, Lokalizacja).")


def usun_klienta():
    try:
        indeks = lista_klientow.curselection()[0]
        wybrane_kino = lista_rozwijalna_klient_kino.get()

        if wybrane_kino == "Wszystkie":
            klient = model.klienci[indeks]
        else:
            klient = [k for k in model.klienci if k.kino == wybrane_kino][indeks]

        model.klienci.remove(klient)
        odswiez_liste_klientow()
        globalna_aktualizacja()
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano klienta do usunięcia.")


def edytuj_klienta():
    try:
        wybrane_kino = lista_rozwijalna_klient_kino.get()
        filtrowani = [k for k in model.klienci if wybrane_kino == "Wszystkie" or k.kino == wybrane_kino]
        indeks = lista_klientow.curselection()[0]
        klient = filtrowani[indeks]
        pole_klient_imie.delete(0, tk.END)
        pole_klient_imie.insert(0, klient.imie)
        pole_klient_nazwisko.delete(0, tk.END)
        pole_klient_nazwisko.insert(0, klient.nazwisko)
        pole_klient_lokalizacja.delete(0, tk.END)
        pole_klient_lokalizacja.insert(0, klient.lokalizacja)
        lista_rozwijalna_klient_kino.set(klient.kino)
        przycisk_dodaj_klient.config(text="Zapisz", command=lambda: aktualizuj_klienta(klient))
    except IndexError:
        messagebox.showerror("Błąd", "Nie wybrano klienta do edycji.")


def aktualizuj_klienta(klient):
    imie = pole_klient_imie.get()
    nazwisko = pole_klient_nazwisko.get()
    lokalizacja = pole_klient_lokalizacja.get()
    kino_wybrane = lista_rozwijalna_klient_kino.get()

    if imie and nazwisko and lokalizacja and kino_wybrane:
        wsp = model.pobierz_wspolrzedne(lokalizacja)
        if wsp == (52.23, 21.00) and lokalizacja.strip().lower() != "Warszawa":
            messagebox.showerror("Błąd", "Podano błędną lokalizację, wprowadź prawidłową lokalizację.")
            return

        klient.aktualizuj(imie, nazwisko, kino_wybrane, lokalizacja)
        pokaz_szczegoly_klienta()
        globalna_aktualizacja()
        przycisk_dodaj_klient.config(text="Dodaj", command=dodaj_klienta)
        pole_klient_imie.delete(0, tk.END)
        pole_klient_nazwisko.delete(0, tk.END)
        pole_klient_lokalizacja.delete(0, tk.END)
        odswiez_liste_klientow()
        if lista_klientow.curselection():
            pokaz_szczegoly_klienta(None)
        informacje_o_wybranym_kliencie.update_idletasks()
    else:
        messagebox.showerror("Błąd", "Wypełnij wszystkie pola dla klienta (Imię, Nazwisko, Lokalizacja).")


def pokaz_szczegoly_klienta(event=None):
    global szczegoly_klienta_tekst
    try:
        indeks = lista_klientow.curselection()[0]
        klient = model.klienci[indeks]

        kino_klienta = None
        for k in model.kina:
            if wyswietl_kino(k) == klient.kino:
                kino_klienta = k
                break

        podstawowe_szczegoly = (
            f"Imię: {klient.imie}\n"
            f"Nazwisko: {klient.nazwisko}\n"
        )

        if klient.kino == "Wszystkie":
            podstawowe_szczegoly += f"Kino: {klient.kino}\n"

        dodatkowe_szczegoly = ""
        if klient.kino != "Wszystkie":
            dodatkowe_szczegoly = (
                f"Lokalizacja: {klient.lokalizacja}\n"
                f"Współrzędne: {klient.wspolrzedne}\n"
                f"Kino: {klient.kino}\n"
                f"Lokalizacja kina: {kino_klienta.lokalizacja if kino_klienta else 'Nieznana'}\n"
            )

        szczegoly = podstawowe_szczegoly + dodatkowe_szczegoly + (
            f"Sieć kina: {kino_klienta.siec if kino_klienta else 'Wszystkie'}\n"
        )

        szczegoly_klienta_tekst = szczegoly
        informacje_o_wybranym_kliencie.config(text=szczegoly_klienta_tekst)
    except IndexError:
        informacje_o_wybranym_kliencie.config(text="Nie wybrano klienta.")


# -------------------------- FUNKCJE DO ZARZĄDZANIA MAPA -------------------------- #


def odswiez_mape():
    aktualny_zoom = widget_mapy.zoom
    widget_mapy.set_zoom(aktualny_zoom + 1)
    widget_mapy.set_zoom(aktualny_zoom)


def wyczysc_mape():
    widget_mapy.delete_all_marker()


def pokaz_wszystkie_kina_na_mapie():
    widget_mapy.set_zoom(6)
    wyczysc_mape()
    for kino in model.kina:
        widget_mapy.set_marker(kino.wspolrzedne[0], kino.wspolrzedne[1], text=f"Kino: {wyswietl_kino(kino)}", text_color="black")


def pokaz_pracownikow_na_mapie():
    wybrane_kino = lista_rozwijalna_kino_mapy.get()

    if wybrane_kino == "Nie wybrano kina":
        messagebox.showerror("Błąd", "Nie wybrano kina. Wybierz kino z listy.")
        return

    widget_mapy.set_zoom(6)
    wyczysc_mape()

    filtrowani = [p for p in model.pracownicy if wybrane_kino == "Wszystkie" or p.kino == wybrane_kino]

    if not filtrowani:
        if wybrane_kino == "Wszystkie":
            messagebox.showinfo("Informacja", "Brak pracowników w systemie.")
        else:
            messagebox.showinfo("Informacja", f"Wybrane kino '{wybrane_kino}' nie ma jeszcze pracowników.")
        return

    for pracownik in filtrowani:
        widget_mapy.set_marker(
            pracownik.wspolrzedne[0],
            pracownik.wspolrzedne[1],
            text=f"Pracownik: {pracownik.imie} {pracownik.nazwisko}",
            marker_color_outside="blue",
            marker_color_circle="darkblue",
            text_color="black"
        )


def pokaz_klientow_na_mapie():
    wybrane_kino = lista_rozwijalna_kino_mapy.get()

    if wybrane_kino == "Nie wybrano kina":
        messagebox.showerror("Błąd", "Nie wybrano kina. Wybierz kino z listy.")
        return

    widget_mapy.set_zoom(6)
    wyczysc_mape()

    filtrowani = [k for k in model.klienci if wybrane_kino == "Wszystkie" or k.kino == wybrane_kino]

    if not filtrowani:
        if wybrane_kino == "Wszystkie":
            messagebox.showinfo("Informacja", "Brak klientów w systemie.")
        else:
            messagebox.showinfo("Informacja", f"Wybrane kino '{wybrane_kino}' nie ma jeszcze klientów.")
        return

    for klient in filtrowani:
        widget_mapy.set_marker(
            klient.wspolrzedne[0],
            klient.wspolrzedne[1],
            text=f"Klient: {klient.imie} {klient.nazwisko}",
            marker_color_outside="green",
            marker_color_circle="darkgreen",
            text_color="black"
        )


def pokaz_kin_po_sieci():
    wybrana_siec = lista_rozwijalna_siec_mapy.get()

    if wybrana_siec == "Nie wybrano sieci":
        messagebox.showerror("Błąd", "Nie wybrano sieci kin. Wybierz sieć z listy.")
        return

    widget_mapy.set_zoom(6)
    wyczysc_mape()

    filtrowane_kina = [k for k in model.kina if wybrana_siec == "Wszystkie" or k.siec == wybrana_siec]

    if not filtrowane_kina:
        if wybrana_siec == "Wszystkie":
            messagebox.showinfo("Informacja", "Brak kin w systemie.")
        else:
            messagebox.showinfo("Informacja", f"Brak kin sieci '{wybrana_siec}' w systemie.")
        return

    for kino in filtrowane_kina:
        widget_mapy.set_marker(
            kino.wspolrzedne[0],
            kino.wspolrzedne[1],
            text=f"Kino: {wyswietl_kino(kino)}",
            text_color="black"
        )


def pokaz_kina_dla_seansu():
    wybrany_seans = lista_rozwijalna_seans_mapy.get()

    if wybrany_seans == "Nie wybrano seansu":
        messagebox.showerror("Błąd", "Nie wybrano seansu. Wybierz seans z listy.")
        return

    widget_mapy.set_zoom(6)
    wyczysc_mape()

    znalezione_seanse = [s for s in model.seanse if s.tytul == wybrany_seans]

    if not znalezione_seanse:
        messagebox.showinfo("Informacja", f"Brak kin z seansem '{wybrany_seans}' w systemie.")
        return

    znalezione_kina = []
    for seans in znalezione_seanse:
        for kino in model.kina:
            if wyswietl_kino(kino) == seans.kino:
                znalezione_kina.append(kino)
                widget_mapy.set_marker(
                    kino.wspolrzedne[0],
                    kino.wspolrzedne[1],
                    text=f"Kino: {wyswietl_kino(kino)}\nGodzina: {seans.godzina_rozpoczecia}\nData: {seans.data}",
                    marker_color_outside="orange",
                    marker_color_circle="chocolate",
                    text_color="black"
                )

    if not znalezione_kina:
        messagebox.showinfo("Informacja", f"Brak kin z seansem '{wybrany_seans}' w systemie.")


def aktualizuj_kino_na_mapie_po_sieci():
    wybrana_siec = lista_rozwijalna_siec_mapy.get()
    if wybrana_siec == "Wszystkie":
        nazwy_kin = [wyswietl_kino(kino) for kino in model.kina]
    else:
        nazwy_kin = [wyswietl_kino(kino) for kino in model.kina if kino.siec == wybrana_siec]
    lista_rozwijalna_kino_mapy['values'] = ["Wszystkie"] + nazwy_kin
    lista_rozwijalna_kino_mapy.set("Wszystkie")


def aktualizuj_liste_seansow_na_mapie():
    unikalne_tytuly = sorted({s.tytul for s in model.seanse})
    lista_seansow_mapy = ["Nie wybrano seansu"] + unikalne_tytuly
    lista_rozwijalna_seans_mapy['values'] = lista_seansow_mapy
    lista_rozwijalna_seans_mapy.set("Nie wybrano seansu")


def odswiez_liste_sieci_na_mapie():
    sieci = sorted({kino.siec for kino in model.kina})
    lista_rozwijalna_siec_mapy['values'] = ["Wszystkie"] + sieci
    lista_rozwijalna_siec_mapy.set("Wszystkie")


def pokaz_szczegoly_kina_na_mapie(event=None):
    selected = lista_rozwijalna_kino_mapy.get()
    if selected == "Nie wybrano kina":
        messagebox.showerror("Błąd", "Wybierz konkretne kino z listy.")
        return

    kino_wybrane = None
    for kino in model.kina:
        if wyswietl_kino(kino) == selected:
            kino_wybrane = kino
            break

    if kino_wybrane is None:
        messagebox.showerror("Błąd", "Nie znaleziono kina o podanej nazwie.")
        return

    widget_mapy.delete_all_marker()
    widget_mapy.set_position(kino_wybrane.wspolrzedne[0], kino_wybrane.wspolrzedne[1])
    widget_mapy.set_zoom(15)
    widget_mapy.set_marker(
        kino_wybrane.wspolrzedne[0],
        kino_wybrane.wspolrzedne[1],
        text=f"Kino: {wyswietl_kino(kino_wybrane)}",
        text_color="black"
    )

    liczba_pracownikow = len([p for p in model.pracownicy if p.kino == wyswietl_kino(kino_wybrane)])
    liczba_klientow = len([k for k in model.klienci if k.kino == wyswietl_kino(kino_wybrane)])
    liczba_seansow = len([s for s in model.seanse if s.kino == wyswietl_kino(kino_wybrane)])

    szczegoly = (f"Nazwa: {kino_wybrane.nazwa}\n"
                 f"Sieć: {kino_wybrane.siec}\n"
                 f"Lokalizacja: {kino_wybrane.lokalizacja}\n"
                 f"Współrzędne: {kino_wybrane.wspolrzedne}\n"
                 f"Liczba pracowników: {liczba_pracownikow}\n"
                 f"Liczba klientów: {liczba_klientow}\n"
                 f"Liczba seansów: {liczba_seansow}")

    tytul = f"Szczegóły kina \"{kino_wybrane.nazwa} ({kino_wybrane.siec})\""
    messagebox.showinfo(tytul, szczegoly)


def podpowiedzi_przyciskow_na_mapie(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
    label.pack()

    def po_najechaniu_kursorem(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def po_zabraniu_kursora(event):
        tooltip.withdraw()

    widget.bind("<Enter>", po_najechaniu_kursorem)
    widget.bind("<Leave>", po_zabraniu_kursora)
    tooltip.withdraw()
    return tooltip


# -------------------------- GLOBALNE AKTUALIZACJE -------------------------- #


def odswiez_listy_rozwijalne_kin():
    nazwy_kin = [wyswietl_kino(kino) for kino in model.kina]
    lista_rozwijalna_pracownik_kino['values'] = ["Wszystkie"] + nazwy_kin
    lista_rozwijalna_pracownik_kino.set("Wszystkie")
    lista_rozwijalna_klient_kino['values'] = ["Wszystkie"] + nazwy_kin
    lista_rozwijalna_klient_kino.set("Wszystkie")
    lista_rozwijalna_seans_kino['values'] = ["Wszystkie"] + nazwy_kin
    lista_rozwijalna_seans_kino.set("Wszystkie")
    odswiez_liste_sieci_na_mapie()
    aktualizuj_kino_na_mapie_po_sieci()
    aktualizuj_liste_seansow_na_mapie()
    odswiez_filtr_sieci_kin()


def aktualizuj_po_zmianie_zakladki(event):
    id_aktualnej_zakladki = zakladki.select()
    nazwa_zakladki = zakladki.tab(id_aktualnej_zakladki, "text")

    # Sprawdzanie połączenia z internetem
    if not model.czy_jest_internet:
        messagebox.showwarning("Brak połączenia z Internetam", "Utracono połączenie z Internetem. Proszę połączyć się z siecią, aby korzystać z pełnej funkcjonalności aplikacji.")

    if nazwa_zakladki == "Kina":
        informacje_o_wybranym_kinie.config(text=szczegoly_kina_tekst)
    elif nazwa_zakladki == "Pracownicy":
        informacje_o_wybranym_pracowniku.config(text=szczegoly_pracownika_tekst)
    elif nazwa_zakladki == "Klienci":
        informacje_o_wybranym_kliencie.config(text=szczegoly_klienta_tekst)
    elif nazwa_zakladki == "Seanse":
        informacje_o_wybranym_seansie.config(text=szczegoly_seansu_tekst)
    elif nazwa_zakladki == "Mapa":
        if not model.czy_jest_internet:
            messagebox.showwarning("Brak połączenia z Internetem", "Funkcje mapy wymagają połączenia z Internetem. Proszę połączyć się z siecią.")
        else:
            odswiez_mape()


def globalna_aktualizacja():
    # Zapamiętaj aktualny stan interfejsu
    aktualna_zakladka = zakladki.tab(zakladki.select(), "text")
    aktualny_wybor_zakladka = {
        'kino': lista_kin.curselection(),
        'seans': lista_seansow.curselection(),
        'pracownik': lista_pracownikow.curselection(),
        'klient': lista_klientow.curselection()
    }

    # Wymuś pełne odświeżenie wszystkich danych
    odswiez_listy_rozwijalne_kin()
    odswiez_filtr_sieci_kin()
    aktualizuj_liste_seansow_na_mapie()

    for funkcja_odswiezajaca in [odswiez_liste_kin, odswiez_liste_seansow, odswiez_liste_pracownikow, odswiez_liste_klientow]:
        funkcja_odswiezajaca()

    # Wymuś aktualizację szczegółów dla wszystkich zakładek
    for nazwa_zakladka, pole_listy, pokaz_szczegoly  in [
        ("Kina", lista_kin, pokaz_szczegoly_kina),
        ("Seanse", lista_seansow, pokaz_szczegoly_seansu),
        ("Pracownicy", lista_pracownikow, pokaz_szczegoly_pracownika),
        ("Klienci", lista_klientow, pokaz_szczegoly_klienta)
    ]:
        if aktualny_wybor_zakladka.get(nazwa_zakladka.lower()[:-1]):
            idx = aktualny_wybor_zakladka[nazwa_zakladka.lower()[:-1]][0]
            if idx < pole_listy.size():
                pole_listy.selection_set(idx)
                pokaz_szczegoly (None)
                # Wymuś natychmiastową aktualizację GUI
                pole_listy.update_idletasks()
                if nazwa_zakladka == "Kina":
                    informacje_o_wybranym_kinie.update_idletasks()
                elif nazwa_zakladka == "Seanse":
                    informacje_o_wybranym_seansie.update_idletasks()
                elif nazwa_zakladka == "Pracownicy":
                    informacje_o_wybranym_pracowniku.update_idletasks()
                elif nazwa_zakladka == "Klienci":
                    informacje_o_wybranym_kliencie.update_idletasks()

    # Przywróć oryginalną zakładkę
    zakladki.select([idx for idx, tab in enumerate(zakladki.tabs())
                     if zakladki.tab(idx, "text") == aktualna_zakladka][0])

    if aktualna_zakladka == "Mapa":
        odswiez_mape()
        widget_mapy.update_idletasks()

    # Ostateczne wymuszenie odświeżenia całego interfejsu
    root.update_idletasks()
    root.update()


# -------------------------- KONFIGURACJA GŁÓWNEGO INTERFEJSU -------------------------- #


# --- Ikona i style aplikacji --- #

def pobierz_sciezke_ikony():
    """ Zwraca ścieżkę do tymczasowej ikony (działa zarówno w .exe, jak i w terminalu) """

    ikona_w_bajtach = b'\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00 \x00\x90<\x00\x00\x16\x00\x00\x00\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00\\r\xa8f\x00\x00\x00\x01orNT\x01\xcf\xa2w\x9a\x00\x00<JIDATx\xda\xed}\txT\xd5\xd9\xff%a\t{\x12B\x12B\xd8\xc2\x1e\xf6]\xf6\xdd\x00"\xb2\x1b@\x02\x04\x08\x8b\x02\xb2\t$aI\x02I\xd8%\xac\t\xa8,*A\xc5\xaa,*\xee\x1b*Z\x8b\xfbRk[\xb1\xfe\xfb\xfd\xdb~\xb5\xb5\xad\xb6\xb5}\xbf\xf3;s\x07\x03&\xb9\xe7\xdc\xb93\x99\xc9\xbc\xe7y~O\xe6\xc9\xdc\xb9\xf7\xce\x9d\xf3\xfe\xce{\xde\xd50x\xf0\xe0\xc1\x83\x07\x0f\x1e<x\xf0\xe0\xc1\x83\x07\x0f\x1e<x\xf0\xe0\xc1\x83\x07\x0f\x1e<xT\xfeQU\xa0\xb6@\xb8@\x94@\xac@\x9c@c\x13\x8d\xcc\xff\xe1\xbd\xfa\x02\xb5\xcc\xcf\xf0\xe0\xc1#\x80Fu\x81\x06\x02\x89\x02c\x04\x16\tl\x168,\xf0\x98\xc0\x8b\x02?\x17\xf8D\xe0W\x02_\n\xfcV\xe0s\x81\x8f\xcc\xf7\x9e\x13xT\xa0H K`\x81\xc0(\x816\x02\x91\x02\xd5\xf81\xf3\xe0\xe1?+;V\xf2\xe1\x02\xab\x04\x8e\x0b\\\x12\xf8Z\xe0\xaf\x02?\x08\x90\x87\xf8\xc1<\xd7W\x02\xaf\x0b\xdc#\xb0L`\x88\xa990!\xf0\xe0\xe1\xc3\x11&\xd0V \xd5\\\xd9\xdf\x13\xf8\x8b\x03\x82\xae\x83\xff\n\xfcY\xe0}\x81#\x02\xb3\x04Z\x99\x1a\x08\x0f\x1e<\x1c\x1e!\x02M\x05f\n<(\xf0\x1b\x81\x7f\xf9X\xe8\xcb\xc3?\xcd-\xc51\x81i\xa6]\x81\x07\x0f\x1e\x0e\xac\xf6}\x04\xb6\t|`\n\x1a\xf99\xbe\x17\xf8\x85i{\xe8\xc1Z\x01\x0f\x1e\xfa\x03\x16\xfb\x1b\x05\xee\x17\xf8}\x00\x08}Y\xf8\x9d\xb9E\x18&P\x93\x7fV\x1e<\xacW\xfc\x11\x02\x0f\x99{l\xaa$\xf8\x93\xc0\t\xc3e8d\x8d\x80\x07\x8f\xebF\x15S]\xbe\xd7\x14\x16\xaa\xa4\xf8\x83@\xa1@7\xf3;\xf3\xe0\x11\xf4\x03\x06\xb3\r\x86\xcb\xb0GA\x82/\x04\xd6\x19\xae\xe0#\x1e<\x82r\xc0\x7f~\xb3\xc0\xcb\x86\xcb\xad\xe6U\xa1\xabZ\xb5\x1a\xd5\x08\xabI\xb5j\xd7\xa1:u\xebS\xddz\x11T\xaf~\xa4\x04^\xe3\x7fx\x0f\xc7\xe0X\x1f\x90\x00\xe2\x0b^\x10H28\xea\x90G\x90\r\x04\xef\xc0\xb2\xff\xbfN\x0bVHH\xa8\x14\xe4\x98F\xf1\x94\xd8\xa9\x07\r\x182\x86\xc6\xdc2\x83n\x9dy\x07\xcdY\xb4\x8e\x16/\xcf\xa1;\xd7m\xa7U\x99\xbb\xe9\xae\x8d{\x05\n\xe4\xeb;\xd7n\xa7E\xcb\xb3i\xce\xc2\xb54\xf5\xb6\xdbi\xf4\xb8\xe9\xd4o\xf0(j\xd7\xa1;E\xc76\xa6Z\xb5\xea\x88s\x87x\x83\x08\xfe\xbf\xe1\x8a8l\xc8\xd3\x82G0\x8c\x01\x02\xcf;\xb9\xea\x87\xd5\xacE\x8d\x9b\xb4\xa0\x1b\x06\x8c\xa4\x89\xc9\xf3\x85 \xe7Pz\xceA\xda\xb4\xed>\xca\xbd\xfbA\xca/8%P,\x91\x07\xec9Y\n\\\xef\xe5_\xc5)\xf9\xd9M[\xef\xa5u\xd9\x07h\xe1\x9dY4~\xea\\\xea\xd5w\x185j\xdcLj\n\x0ek\x03\xe7\x05z\xf3\xf4\xe0QY\x07\xac\xdf\x88\xde\xfb\xb5\x13BS\xa3F\x185k\xd1\x86\x86%M\xa0ywdR\xc6\xe6C\xb4e\xd7\xfdRp\xddB\x9e\x0b\x08!\xf6\x04W\t\xc2$\x85\xcd\xe2\x1a\xeb\x04\xb9\xa4\nmb\xf0\x88q\xd4\xa4Y+y/\x0e\x11\xc1g\x86+\x90\x88\xc3\x8byT\xaa\x11.\x90c\xb8b\xea=\x12\x92\xf0\x88(\xea\xddo8\xcdJ\xbb\x8b2\xb7\x14\x9a+\xbc)\xf0\x1e\n\xbb\x0e)\xe0\x9ax\x9d\xb1\xb9P\xdc\xcbj\xea\xd1g\x08\xd5\x0fo\xe0\x04\t\xc0\xfd\xb9^\xa0.O\x1b\x1e\x95a\xc4\x0b\x1c5<\x08\xdd\xadR\xa5\x8a\xd8\xd37\xa1\xe1\xa3&\xd2\xd2\xbb\xf2\xc5*|\xc2\xe7BoE\x069;O\xc8{\x1bz\xe3\x04j\x18\xdd\xc8\x89\xd0\xe2\x03\x02\xd1<}x\x04\xf2h-\xf0\x84\'\xc2\xd00&\x8en\xbc\xe9VZ\xb5\xfenS\xe0\x8a+\\\xe8\xcb$\x03S+X\x91\xb1\x93\x86\t\xb2\x8a\x8c\x8a\xf1\x84\x04\xfec\xb8\x02\xa2\x9a\xf24\xe2\x11\x88\x039\xf9\xcf\xd9\x15\x80:u\xebQ\xff\xc1\xa3i\xf9\xba\x1dWWZ\x7f\x15\xfc\x9fj\x05."X\xbaf+\xf5\x1d\x98D\xb5j\xd7\xf5\x84\x08\xce\x18\xaeLC\x1e<\x02ft0\\\xc57\xf4\xddx\xa1\xa1\xd4\xb6}Wi\xd8\x83\xaa\xef\xcf+\xbe\n\x11`k\x00\xd7b\xcb\xd6\x1d<q#>%\xd0\x92\xa7\x15\x8f@\x18\xad\xec\xae\xfc\xf5\xeaG\xd0\xa8\x9b\xa7Q\xe6\x96\xa2\xab\xea\xb4\xa3(\xd5\xfdw-r\xef>\xe9\x95\xad\x01\xdc\x92#FO\xa6:u\xeay\xa2\t4\xe3\xe9\xc5\xc3\xdf\r~g\xecL\xf0\xe6-\xdb\xd1\xbc\xdb3i\xcb\xee\x07\x1cQ\xf7\xdd\xbe}\xb7_\x7f\xcb\xee\xfbe\\\xc0\xfa\xdc\xc3R\x18\xd7e\xef\xa7\xb5Y\xfb$\xf0:}\xf3!\xf9^\x968\x06\xf7\xe0\x8e\x1d\xf8\x91\x18<\xbf\x1f\xdc\xc3\xec\x05k\xa4\xeb\xd0&\t<\xc4\x86A\x1e\xfe:"\x0c\x97\xb5_kR\x87V\xadJ=\xfa\x0c\xa6\xd5\x1b\xf6x\xbc\xea_u\xcf\t\x01\x860\xdf\xb9v\x1b\xcd\x98s\xa7\xd4*\xfa\xf4\x1fA\x89\x9dzR\xb3\x84\xb6\xd2\xa3\x00\x03\x1d\\\x8a\x00^\xc7\xc65\xa5\xe6\t\xed\xa8C\xe7^2\xa0\x08\x91\x80\xb7\xcd]!m\x10\x1b\xf2\x8e8\xe6n\x04)\xad\xcc\xdcM]z\xf4\x97\xdb\x1d\x1b\x86Ax\x07\xea\xf0t\xe3\xe1O\xa3\x86@\xbe\xc0\xbfu&4\xa2\xe9F\x8c\x99B\x1b\xb7\xdek{\xaf\xef\x16z\x04\xe8\xac\xd9\xb4\x97f\xa4.\x97\xe1\xbf\x10\xe6\xba\xf5\xc2\xa9Z\xb5\xea\xb6\rp\xd5\xaa\xd7\x90\xdb\x92\x84V\x894h\xf8X\x9a9o\xa5\xd0\x18\xf6\x9b\x1a\x82}2\xc0w]\x9fwX\xba\x0cm\x04\x11\xa1\xe0H\xa6\xc1\xf9\x03<\xfch\xcc\x13\xf8\xd6\xd0\xb2\xf2\xd7\xa7\t\xb7\xce\xa3\x9c\x9d\xc7m\t\x92;:oC\xfe\x11\x19\x95\x07k{tl\xbcG\x02o\x85\xea\x82\x10\xa0)\xc0;1wq\xba \xae{l\x13\x01>\x93\xb3\xe38\xdd<i\xb6\xcc]\xd0\xbc\x17\xe4P$\xf3\xb4\xe3\xe1\x0fc\x90\xe1*\xad\xad<\x81\xeb\x87GR\xf2\xac%r%\xd5\r\xd7u\xef\xed\x11\xfa;y\xfaBj\xdd\xae\xb3\xcc\x050|\x9c\xd2\x8bk\xb6K\xecF\xb7\xce\xbc]F$\xda\xb1\x15\xe0xh.\x93\xa6-\x90\x84\xa8y\x0f(m\xde\x8b\xa7\x1f\x8f\x8a\x1c\xc8\xe5\x7f\xde\xd0\xb2\xf4G\xca}\xb9]k:\xf6\xe3\x10|\x18\r\xabV\xadZ\xe1\xb9\xfdU\xabU\xa3\x16\xad\xdaK"\xd8\x98\x7f\x8f\x8d\xad\xccII\x84S\xc5\xe7m\x90\xc0Y\x83\xb3\x08yT\xd0@r\xcf\x0eC#\xab\x0f\x13\x1c+\xbf\x1du\x19+e\xaaP\xbb\xdbu\xe8&\x85\xce\xf0\xb3"\x1f\xd8z\xc0\xc8\x98\xb6d\x83\xb4\xf6\xebj\x03 \x01h\x02H;6\xf4\xb2\x087\t\x84\xf2t\xe4\xe1\xebq\x8b\xa1\x91\xcf\x1f\x16VK\xa6\xeaJ\xb5_\xd3`\x06\xc3\xdb\x90\x91\xb7\xd8Y!}\x0e\x18\x1e\x87\x8f\x9a$]\x8dz\xda\x80\x8b\xe4\xc6NL\x91\xb6\x06\x8dk\xfe\x8f\xe1\xaa\xa3\xc8#\x80\x06\xd2=\x91\xed\x85VS1\x86\xab\xc3L\xc9>u1\xe6{u\x0c\xffL\r\x85\xbf\xff\xa2\xb2\x9a,T\xf5\x917M\x95Qq\xea{~\xd7q\xf3\xc5\x8a\x8a(:$\x04\x19\x01R\xf2\xabJ\x95\x10i\x9b@\x81\x11\x1d\x1b\x07\xb4\x86\xec\x1d\xc7d\x9a1\n\x9bh\\\xf3\x82\xc1\xf1\x01~;P\xe2\x1a\x11\\C\x05\xe6\x0bl\x11\xb8O\xe0\x9c)D\xa8w\xff\xb9iH\xfb\x8d\xe1\xca\t\xc7\xff^3\xf7x86\xc7\xfc\xec\x10\x81&\xe69+j\xa0IG\x96\x8e\xea\xdf\xf3\x86\xa1\xa6\xab\xef\xa4\xba\x85|\xe7q\xa11\xa4I?\xbd\x11\xa0\xb5\xff\x1aD\xc5H\xdb\x80+\xa4Y\xfd\xbb#\x86\xa1s\xb7\xbe:\xd7\x82\xfbu5\x8b\x9a\x7f\x0c\x08\x08J^\x8d2\xf7gO\x98\x02\xfe\x8d\xa1\xe9\'/\xe5GF\xae\xf8/\xcdsn0\xaf\xd1\xc8\xbc\xa6\xaf\xc6\r\x02WT\xef\xbbE\xcb\xf6\xb2\xec\x96\x8e\x00\x80,\xa0F;\\uG\xae\xaa\xb5k\xd7\xa6\x88\x88Hj\xd80\x9a\xa2cb%\xa2\xc4k\xfc\xafV\xad\xda\x8e\x97\xfd\xaaY\xb36%\x8dM\x96\x11\x86\xea\xcf\xa0\x98V\xa4\xef\xa4\xf8\xa6\t:\xd7\xc2\xbc\xe8\xc4\xe2Wq\x03]i\xc7\n\x14\x18\xae~u\x7f\xf5\xc1*\x83k\\\x16\xd8c^;\xca\xcb\xdf\x11u\xfb\x8f\x1a\x1a\xb1\xfdH\xeaQ\x8d\xf0\x93\xab_\xdea\xea;(\x89BC=\xb7\xf0\x87\x85\x85Q\xe3\xc6\xf14d\xe8p\x9a;\x7f\x11\xad\xdf\xb4\x85\x0e\x14\xdeG\x0f\x9d>C\xe7\x9ez\x81.<\xff\x9a\xc4\xd9\xa7\x9e\xa7\xe2G\x9e\xa0\xfd\x87\xee\xa1\xcc\r9\x94:w\x01\r\x1c4\x84\x1a\xc5\xc5Q\x8d\x1a5\x1c\xf1\x14\x0c\x1a~\xb3\x8c\x1b\xd0!\x81\x94\xf9\xab\x05aie\x12\xee3\xb8\x9a\x90\xcfW{4\xaaDgZT\xb7\xfd\xd6\xa88\x95\xf3[s\xdb\x00U\x10\xad\xac\xbdQw~\xb4\xa1\xd8\xb0#44T\x86\xd3\xaa\x1a\xfd\xdc\xaao\x9f~\xc3=Z\x85aoh\xd2\xb4\x19M\x9e\x92L\xbb\xf6\x1c\xa0\xf3\x17^\xa2K\xef|H\x1f|\xf2\x1b\xfa\xf8\x97W\xe8\xa3\xcf\xbe\xa4\x0f?\xfdm\xa9\xc0{8\x06\xc7\xbe\xf9\xf3\x0f\x041\xbc@\xdbw\xed\xa5I\xe2\\M\x9b6\x97\xdf\xc9\xee}\x81\xd0\x10@\xe4r\x15\xaa\x91\x00\x8c\x82\xc3\x92&J\x9b\x82\x86Ap \x8b\xa5o\x04\x1f\xea\xd6Vs\xcf\xfe_\xc3\x7f\xf6\x9e\xb8\x97O\x05\xf2\xcc{t\x8a\x08`wxD\xf5>\x10$\x93\x99[\xa44\xd9\xddj?\xa2\xf9\xec\n?\xdcp\xdd\xba\xf7\xa4\xf5\x1b7K\xa1\xff\xc5\xfb\xbf\xbc*\xec\x10\xe8\xf7?\xfe\xb5\x16\xf0\x197)\\\x16\xe7\x82\xc6\xb06}#u\xee\xd2U\\\xab\x9am\x12\x18<|\x1cem?\xaa\xfc\\P\x90\x14q\x06\x1a\xd7\x81\xcd\xa8\x06\x8b\xa8\xf7F\x0b\xd3(\xf7E\x00\x18\xa2~e\xda!\x12\x1c\xf8\xdecL;\x86\x92+l\xfe\x92\xf5\x8a\xaa\xbf+$\x16{~;j?\xbc\x03\x1d;u\xa6\xac\xcd[\xe9\xa5\xd7\xde\xbe\xba\x9a\xeb\n\xbc\x15\\D\xf2[z\xf1\x95\xb7hcv\x1e\xb5O\xec`\x9b\xa8\xa0\x19\xc10\xa8\xba\x15@\xfd\xc3\x9a\xb5j\xebt\x1f\x1a\xccb\xea\xfc\x80\xdbn\xae\xc0;\x01f\x8d\x86F\xf0\xae\xe1\xaa\xc8k\xb7\xd0$\xf6\xfe\x0f\xa8^s\xe0\xb0\xb1R}Uu\x7f!>\xc0Ne\xdd\xa8\x86\ri\xe1\xe2\xa5r\x1fow\xa5\xb7\xab\x19<\xf9\xcc\xcb\xd2V\x10\x11\x19\xa9o\x18\x14\xc2\x9c\x9cr\x87\xf2V\x00\x04\x89B\xa8\x1a\xd7(d[\x80\xb3\xa3\xbb\xc0)\x81\xef\x02\xd5%%\xf0\x0f\x81b\x81\xae6\xbe\x7f?\xc3\xd5\xc0\xc2\xf2:h\xa2\x01\x0b\xb6J\x10\x0c\x8e\x99\x7f\xc7z[\xae\xbe\xae\xdd\xbaS\xd1=\'\xe8\xdd\x0f\x7f\xe5\x95\x15_E#\xb8\xfc\xc1\xe7\xd2p\xd8\xa1c\'\x1b\xe4\x15+\x9b\x94(=\'\xa1I-Y\x9dG\x11\r\xa2U\xcf\x7f\xc5\xe6\xef\xcc\xa3\x94\x95/\xd5\xdc\xe7W\x96\xbet\xb0\x0f\xcc1\xbf\x9b\xaa\xbdc\x87\xaa:\x8e\xdc{U\xa3\x1f\x8aqh\xeeo\xa5\x91\xef\x96\xf1\x93\xe4\n\\\x11\x82_\x9a6p\xf6\xc9\xe7i\xf4\x98\x9b\xb5\xed\x17m\x13\xbb\xca\xa4&\x15M\x00\xc6\xd4!#\xc7\xeb\x9c\x7f#\x8b\xafg\x03\xd1x\xbb\xbce\xd9\xc7^\x10~\xe7\xba\xf5\xea\xcb\xec\xb8\xf0\x88\x06\x12x\x8d\xff\xe1=/\xa6\xb6\xfe\xcd\xfcn1\n\xcf\xa1\xb9\xc0\x87*\xe7E\xaa\xac,\xec\xa10\xa1\xb1\x07\x86A\xcc\xd0\x88\xf0\xab^\xa3\x06\xcdN\x9dO\x17/\xbd[\xe1\xc2\x7f\xbd6\xf0\xca\xc5w(y\xfaL-\x03!\x08c\xe4\x98)J\x9e\x12h\nhi\xd6@h\x0e\x8a\xe7\x7f\xcb\xe0\xe6\xa3\xb6G{\xc3\x15l\xe3\x88u\x1f\xcd&!\xdcm\xdaw\xa2\xc1\xc3\xc6\xd0\xe4i\xa94o\xf1]\xb4b].e\xe6\x14P\xce\xf6"\xca\xddu\xaf\x04^\xe3\x7fx\x0f\xc7LJN\x95\x9fi\xd3\xae\x93<\x87\x83\x8d+Q]\xe6q\x81v\x16\xcf\x02\xda\x82BM\xff*t\xe3MS\x95\xb3\xfa\x90\xc3_[\xa3>\x1e\xfc\xf1\xd8\xef_z\xe7#\xbf\x12\xfe\x92$\xf0\xc6\xdb\x1f\xd0\x9c\xb9iZ$\x80\xec\xc8\x05\xcb6*\x19LA\x14\x88\'\xd0\xd8\xf2MaQ\xd6\x1f}\x05^7\x1c\x08\xfe\x88k\xdc\x94\x06\t\xe1M]\xb8\x8a6\xe5\x1f\xa4\xdd\x07\x8b\xe9\xe0}\x8fS\xd1\xfd\xe7\xa9\xe8\x04p\x8e\n\x81\xe3g\xaf\x85\xf8_\x91\xc4yy\xec\x01\xf1\x19|vS\xdeAJ]\xb0R\x9cs45\x12\xe7v(+\x0e\xb1\x03}\xca\xd9\x02\x15\xab\x9c\'R\xecO\xb1BY\xedi\xdd\xfe~T\xfe\xd5Q\xfbg\xcd\x99Go\xfd\xe2#G\x0c}n\xf7\x1e\xec\x07\x80\xdb]\xe8\x0c\t\xbcO\xc9\xd3fjm\x07:v\xed\xa3\x14*\r\x92\xb8}\xe5\x16\x19`\xa5x\xee#l\x0c\xd4\x1bC\x04\xde\xf7D\xa0P\xcf\xbeG\xef\x014W\x08}\xde\xee\xfb\xa4\xf0B\x90\x0b\x8f\xbb\x04\xfd\xd0\xb13\xb6\xe0"\x07\x17)\xe0\x9c87\x88\xa5{\xaf\xfe\xf2\x9a\x1e\x92\x00\xbc\x04\x83Jy\x1e\xa8\xed\xff\xa5\xca9PGO\xc5\xf2\x8fI>iZ\x9a\x96&3~\xc2\x14\xc7\xd4~\x10\x88\xdb\xa7\x7fk\xf2\x0c)\xac\x88\xfe{\xea\x99W\x1c#\x97\x97/\xfe\x9c\x92F\xdd\xa4Uih\xda\xec\xa5JZ\x00<\x02\xddz\r\xd4\xb1\xf7\xb4`\xb1V\x17\xfe\x8f\xec\n\x11|\xdf\x03\x87&\xd1\xaa\x8c|*8\xfc\x88ku\xf7@\xe0U\x08\x01\xd7\xc0\xb5V\xa6\xe7\xd3\x80!I\xf2\x1e< \x81\x0fK\xf1\x1f#\x01\xc92\x7f\x01\xa9\xbes\x16\xae\xbb\xda/\xaf<\xe1G\x9a,\x9az\xaa\xde\x17\x82{\x9ez\xf6\x15G\x84\xff\xbd\x8f\xbf\xa0={\x0b\xa9u\xeb\xb6\xd7d\x17b\xb5NL\xecH\x87\x8a\x8e:\xb6\x1dx\xe2\xfcs\xd4^\x9cS\xf5{\xb6j\xdbIjFVZ\x00\x9e1\n\xaaT\xab\xaed\x1fB\xfd\xc0i,\xdajj\xbf\xad\x95\x1f\xfe\xeb^7\x0c\x12\x82\xbf\x95\xf6\xdf\xfb3)\x94\x87\xbc(\xf8e\x11\xc1\xfe{~F\xab\x04\x11\xf4\xec3\xd0\x93n\xb5\xd0\x04\xdc-\xaaQ\xf0\xe3\xb8\xca\xe7P\x9dGe\xf2b{\x80\x0c?\xd5\x80\x9f\x86\xd11t\xe4\xbe\x07\x1cS\xcfO<\xf8\x88\xcc\r(\xebz-Z$\xd0\xc3\x8f\x9eu\xecz{\x0f\x1c\xa1\xf0\x88\x08e\xa3\xf0\xb4YK\x95H\x14\xd1\x81q\xf1-t\xf2\x03BX\xc4\xcb7\xf8\xd9\xda\xf37i\x96 \xd5\xf0\x82\xa2\x87]\x82\xef#\xa1/\x0b\xb8\x87=\xe2^R\x17\xae\xa4&z\x99d%\x81\x14e\xe4\x12 \xcb\xf0c\x95\xcf\xa0\xe1\x85\xb5\xf0\xbb\x12}Z\xb6\xe9\xa8\x1c\xe1\xb7\xf8\x8e;\xe9\xbd\x8f\xbepD\xed\x7f\xe7\xbd\xcfh\xc2\xa4\xa9\x96\xd7\x9d\x99\x92*\xfd\xfbN\\\xf3\xf2\x07\xbf\xa4Ys\xe6+?\xfb\xf6\x1d{\xd0&\x05[\x00\x8c\x81\x03\x87*o1\xde6\xb8V@\xb9\xae>\xed\xe6\x95P\xbf\xfa\x0f\xbe\x91\xb2\xb7\x15z\xbc\xb7\xf7\x86F\x00do-\xa4~\x83F\xdau%"\xe6?\xc5P\x08\xfdET[\xda\xd2\r\x96+\x17\xde\x9f\xbd\xe0.\xe5\x14\xdf.]\xbb\xd1\xb3/\\tl\xdf\xff\xe2+\x97\xa8eK\xeb\x86\x1c\x9d:w\xa1W^\x7f\xc71{\xc0\xf9\xa7_\xa2\xb6\xed\xd4b\x1dP\x0e\x0c\x05P\x94\x9f\xa5\x9a\xa6\xf7\'\x81\xfe,\xea\xa5[\xb8w\x9b\xee0\r\xb7M8M\x9d1_\xac\xfa\x8fHk\xbd\xbf\x08\xfeO\x88\xc0\xd4\x06p\xaf\xb8gM\x02\x80\xdb\x0f\x05J~\xb0\xd6\x82Z]\xad\x8ak\x95\xd9\x86\xe6\x1c\xaa.\xbf\xdc\xfc\x9d\x8e\xb9\xfbp\x9eg\x04\x99\xc46\xb2n\xdb\x9d\x90\xd0J\x92\x85Sa\xc5\xb8v\xc6\xfal\xe5\x02\xa6\x83\x86\x8d\xb5\x8c\x0bp\x05Q\xed\xa7\x98\xd8xUw\xefb\x16\xf7\x9f\x8eT3 FY0bb\x1b\xd3\xa2e\x99t\xf0\xe8\x13~\xb5\xea\x97\xa7\r\xe0^\x17.\xcb\xa0\xe8\xd88\xaf\x04\x15\xf5\x1b4Ji\xc2\xde\xb5\xa1@\xec\xe9\xd5\xee\xa1g\xcf\xde\xd2\x92\xee\x94\x10\xe2<\xaf\xbe\xf1\x0b\xea\xdc\xa5\x9b\xe5\xb5\xfb\xf6\x1b@\xaf\xbf\xf5\xbes\xd7\x16\x04\xf0\xdcKoP\x87\x8e\x9d\x95\xbe{\\|s\xb9\xc7\xb7"T\x94W\xeb\xde{\xb0\xea\xeft\xc8\xe0\xc2\xa1\xd7\x0c\xc4\xf6k\x85\xf7\xc67m!\xad\xed\x81 \xf8\xa5\x11\xc1\xcauy\x14\xdf\xa4\xb9\xa3\xc2\x0fc\x1eJt\xa3\x8f\x9e\x95\xca\n7\x97J\xdc\x02V\xcaM\xd9y\x8e\x07\xfb\xc0\x96p\xfb\x92\xe5\x96\x91y\xab\xd7f:\x9eT\x84\xf3\xad^\x93\xa9\x14\x1bP]\xa8\xf5\xc8\xfe\xb3\xde\x06\x9c\xa2\x9b\'\xceR\xad\x95\x88Z\x15\x11,\xf6\xaeQW5\xb8\xc5\x8d\xc6Bp\xeeZ\xbf\xdd\x0b*\xff\xd9\x9f\x06\x01\x99\xc0{No\t\xf0\x1d\xe2\x9b\xb4p\x8c\x00\x10\xc9\x87\xc0\x14\xab\xe0\x1fh\x08\xd0\x14T\xce\x99\x90\xd0\x92\x9ev\xc8\xed\xf7\x93m\xc0\xf3\x17\xa9_\xff\xb2}\xe8C\x87\x8d\xa4\x17_}\xcbq\x02p\xb9\x05\x9f-\xd7\x03Q\x12\x88\xf9\xb7\x8a\x07\x00A \xe5:\xac\xa6R\x9a0\xb6s\t,\xfa\xae\x816V\xdf\xe9\xa8\xfd+\xd3\xf3\xa4\xb1\xcf\x19\x03\xdd930\xe8,\xed=r\x9av\x1ex\x90\xb6\x15\x9c\xa0\xfc=\xc7$\xb6\xed=!\xff\x87\xf7\\.>W\x10\x91\x13\xaeE\x90\x004\x01\xa7\xb6\x03\x8d\x1a7\xb3Lf\xc1{(\x0c\xd2\xb4yk\xa5sN\x9b\x91"\xa3\xf3\xbc\x95\xbc\x83b!\x93\xa7N\x935\x01k\x84\x85\xc9\xb2a11\xb1\xf2\xbaO?\xf7\xaaWR\x8a\xdd^\x88q\xe3\')\xc7\x04XU\x0e\x92v\x80M\xfbTs\x03`\xcc\x1d\xc6\xa2\xefb\xc1\xcb:\x06?\xec\xf9=U\xfbK\x06\xedd\xe5\x1f\xa2y\x8bWS\xd2M\x93e\xc4`B\xabv2\xac7\xaaa\x8c\x04^\'\xb4j/\xde\x1bH7\xde4\x89f\xa7-\xa7\x8d\xb9\xfb\x1d\x0b.\xc2\xe7\x17.\xcd\xb0c\x18\xfci\x08k\x97>\xb2\xba\x8d\xbb\x84wY\xbe\xff\xa5w\xe5+\xd5\xf4\xafY\xb3&\x15\xec+\x92\xa1\xb9\xde\x8c\xd9\xff\xf9\xbb\x9f\xd2\xe9\xc7\x9e\xa4\x9dw\xef\xa7]{\x0e\xd2\xcf\x9exZ\n\xe8\x07^\xcc1\xc0w\xca\xdb\xb6\x9b\xaa+\x04\xf0 \xe7ce\xc6.K\x02\x00I\xa0\xfc\xb8\xa2QwN\xb0\x0b?\x82!\xb2\r\xc5\x04\x1f\xb8\xfa`A\x87\x11\xcdS\x97\x1c\xc2vS\xe6.\xa3n=\xfbQDd\x94\x96k\x0e\xed\xb31!\xba\xf7\xeaG)\xf3\x96\xc9s\xb9\xcfm\xf7\xbe\xf0\x9d\xf0\xdd<\xcd6Db\x8aJ\xe4Zr\xca\x12\xa5\xd0_\xd4\xf2\xf3\x86\xfa_^\xb9\xaf\xaby\x00^.&"\xb7\x01\xe7\x9e\x91\xda\x86\x9a\x1d`\xb5\xa5\x1d\x00\x1d\x88T=+\x02\x19\xc1N\x00\xa8\x8f\xa7\\\xc6\x0b~~\xe9\xea\xb3%h\xae\x15?\xff\xee\xa34y\xda\\j\xd6\xbc\x95#Unq\x0e\x94\x8aF\x86 \x88\xc0\xee\xd6\x00\xdf\t.B\xc4\t\xd8\xbd\x17\x18\x9f`\x84R1\x00"\xe5U)\xa0h\xe4(z\xeb\x17\x1fk\xab\xe18\x1e\xe5\xba|U\x11\xc8\xce\xb5p<\xbc\x0b\xf02\xa8<\x8b\xb1\x13R\x14\x9e\xed)\x99\x81\xc9\x11\x81j\xab\xffV\x9d\x08?\x19\xe4c\xc3\xe8\x07\xe1\xdaw\xe4Q\x9a\x7f\xfb\x1aj\xd9\xba\xbdNEWu\xe1\x0b\t\xa1\x16-\xdb\xcak\xb8m\x05v\xec\x01\xd9[\x0f\xd9\x8e\x18\x84\xf60}\xf62\xcbU\ny\xffh\x0c\xa2r\xce\x05\x8b\x96h\xad\xfe8\x16\xc5?Q\x0b\xf0\xf9\x97\xde\x94\tCnas^\xf0]\xf7\xf5\xda\x9b\x97\xc5\xb5\xde\x90nJD\xfa\xe9j+3g\xa5\xaa-@C\xc6(\x18\x02O\xc9~\x82\x8a\xd5\x8a\x8b\r\xf5"0\x95n\xb4Uu\xfb!\xba\n\xe1\xbdv\x8c~\x10\xc4\xad{\x8e\xd1\x88Q\xe3}\xd2\xb2:,\xac&\r\x1by\xb3\xd04\x8e\xd9\xbe_\xa4\x17\xdb\xc9\x1d\xc0\xf7C\xcd\xff\xf2\x08\xc0]\xed\xb7mb7%\xf7_\xf6\xe6\xadB%\xbf\xa2(L_\xd0\xfd\'\x1f\xa5)S\xa7\xcbH\xbb&M\x9aR\xaf\xde7\xd0\x8aU\xeb\xe8\x05\x07\x03y\xdc\x84\x82@\xa2%\xcbVR\xf7\x1e\xbd(^\\\xab]\xfb\x0e\xd2px\xea\x91\'\x94\xcf\x83\x92\xe3k\xd6mPz\xbe\xe8\x0c\x94\xbd\xfd\x98\xa5v\x952\x7f\x95\xdc2(\x9c\xf3I\xc3~M\xc8\x80\x1f\xabU\xf7\xfeH\xecAl\xbf\xee\xaa\n\x01\xdc\x90\xbb\x9f:t\xea\xee\xf3>v\x1d:\xf7\x90\xd7\xd6%\x01\xf7V\x00\tDv\\\x80w\xac\xca-\xd7\x05(=\x00[\x8a(\xbeYK\xeb4\xea:u\xe9\xf0\xbd\'\x94\x0c\x80\x10\xc8\xbb\xf7\x1e\xa2\xc6\xf1MJ\xdd\x9a\x0c\x196BZ\xf4\x9dJ\xea9\xf7\xf4\x0be\xba\x0f\x9b7oA\x07\x0b\xefS"\x1c|7\xdc7\x8c\x9dV\xcf\x039\x13\x1b\xf2\x8f\x94kc\x01\x01\xa0\x1bqM5W \xf2]"\x83Q\xf8\xd1-\xe75C1\xa5\x17\xe9\xbc\xba\x89=\x10\xbc\xf4\xac\xdd\xd2\xa2\xefK\xc1\xbf\xc6\x7f.\xae\x8d{\xd0%\x01|W\x048\xa1\x0c\x99\xa1\x99\xfe\xbc2s\xb7\xa5\xa5\x1aQmQ\xd1\xd6!\xb8\x91\r\x1a\xd0\xa3\x8f?e)\xb4x\xff\xcc\x93\xcfQ\xabV\xe5\xa7\x14\xcf\x989[n\x0f<]\xf9\xdf\xbe\xfc\tM\xb4H"J\xec\xd0\xc9t!Z\xdf\xfb\xfd\'OS}\x05\x0fL\xe3&\t\x96!\xd6 _\x14\x0bU\xac\xac\x04\xefWP&\x05\xa1e\x96R]\xbf\x81CF\xc9\x94^\xddU\x14\xaboE\n\x7fI\x12\xd8\xb0e\x9f6\t \x95x\xc0\xe0$\xadk\xa1v\xe1\x9aM{-\t`\xcd\xa6}T?\xa2\x81u5\xe1\x98X\xa5U\x1b\xef#Z\xcf2F\xa1Q\x1c=q\xeeY\x8f\xb4\x00|\xf6\xd4\xe93\xd4 \xaa\xfc\xaa\xc5!b\x0f\xbe1+\xd7R{\xc1\xf9\xe0rl\xd0\xc0\xba\n2\xaa+\xbbZ\x8c\x97\xff|Q\x85I\xb1m:j]\xc4\x04\x9b\xf0\xc3\xf8W\xa02\xa1QUGw\xf5w\xef\xf9\xa1\x82W\xb4\xf0_\xdd\x0et\xea!\xefIg\x0b\xe3\xd6\x02t*\x0b\x85GF\xc9\x84\x14\xab\t\x8a\x1c\x00\x95\x12Vqq\x8de\xcc\xbc\x95\xc0\xc2\xf06q\xf2\xad\n1\x05\xb5d>\xbe\'1\x05\xf8\xec\xd6\x1d{\x94|\xf7\xb7\xcd\x9c#\xed\x12\x96\xdb\x89\xa7^\x90AHV\xe7k\x10\x15k\x99\x13\x80\xf7Vf\xeeR-\x04\x83\xe6\xa1\x8d\x82\x8d\x00\xd0\xa5\xf7=\x95\t\x8d\xa0\x1c\x04\xdb(\xbb\xd5\xccH\xbe\xe1I\xb7x\xb4\xe7\xc7D\x8d\x8c\x8c\xa4\xe8\xe8\x18\t4\x9a\xa8\xe9\x91\x01\xb1\x8a\xbc\'x"T\xc3\x89A\x16\xf8\xee(/\x16\x08\x040I\x85\x00j9I\x00\xd6\rBoK\x99\xa3fO\xa88\x02\xf8,\x18\t\x00\xed\xb3-\xbb\xf4"I\x055\xfc\xf4V\xffs\xd2\r\x17f\xa3\x85u\xed\xdau\xa8w\x9f\xbe29\xa5`\x7f\x11=\xfc\xe89Y\xf6\n\xc0k\xfco\xb1x\xafw\x9f\x1b\xe4\xb1v,\xf4\xf3\xefX\xab\xb5\x15\xc0wG!\x11\xd5B\xa3r\x0b\xb0\xd1\xc9-@\x8c\xe2\x16\xe0K\xbak\xedzK\xd2\x95[\x80\xf3\x9eo\x01\x1e:}\x96\xa2\xa2\x1aZ6BE\xbb0?\xdf\x02|\x10\x8c[\x80\x8dj1\xedM\xcd\xc0\x1a\xf5\x15\x13\xc7\xb7h\xd5VK0\xa1J\x0e\x1d6\x82\xf6\x1d\xbc\x87^{\xf3\xdd\xab\xd1h\xa5u\xa9\xc5_\xf8\x9cq\xec\x90\xa1#\x94\xd4\xd0\xeb\xed\x01\x08D\xd2\xf9N\xb9\xbb\xef\x95\xcf\xc2\xdf\x8d\x80h\xe7\xdd\xaa\xb5\x0f\x8d\x80\x16\x1a\x07:\x03\xa9\x1a\x01O<XaF\xc0\x9f\x0b4\x0c&\xe1\x87\xcf\xf3q\x95\xc9\x8c\xba\xfb\xa8\xb4\xab\xb3\xf7G4\x9e\x8e\xea\x0f\xf5~m\xc6Fz\xfd\xd2{R\xc0U\xdcF8\x06\xc7\xe23\xa8b\x8bs\xe8\x04\x0b!\nQ\xc7\x16\x80g0h\xe8(\xc7\xdd\x80(\x1a\xa2\xe2\x06D\xab/u7`!\xc5\x97\xe6\x06\x14\xdf\xdby7\xe0\x8b\xd4\x7f\xc0\xa0\xd2\xdd\x80-\x12d1\xd1\x00p\x03^\x0c67`\x82J\xf0\x0fb\xd4S\xa5\xfa\x7f^k\xf5G\xb4\xa0\xaa06m\xda\x8c\xf6\x89\xfd\xa8\xdd(5\xf7g\xd0\x87\x0e\xe7R\xben\xb3\x96Z\x9a\r\x9e\xc1\x9c\x05+\x94\xe2\xf6\xfd!\x10\xe8\x81\xe2Gi\xca\xad\xd7\x06\x02\xad\\\xed\x9d@\xa0g_x\x9d\x96\xde\xb9\xeaj P{w \xd0\xe93\xde\t\x04\xea\xae\x18\x084\x8f\x03\x81\xca\x1a\xa3\x05\xfe\xd7P\xc8\xbcB\xd3\x0e\xd5\xfd2\xf6\xca)s\x97\xaa\x86_\xcaU\x1bj\xbcS\xab\x11\x88\xa4\xa1\xa2&\x80\xdc\x01$\x10\xa9\xda6\xf0\x0c6\xe5\x1d\x90\xcf\xc4\xc9P\xe0^}+[(\xf0\x9bf(\xf0\xe7^\x0b\x05\x1e\xe0|(\xf0\xfd\x025\x82\x89\x00\x96\x0b\xfc\xd3\xea\xc1\xa0]\x17\xba\xee\xa8\xac\x92nk9\xb2\xfaT\xf7\xfcP\xdd\x9d\x9e\x8cXETm\x02\xb0\xec\xabz7\xf0\xfd\xf0,\xda\xb4\xeb\xe8l2\x90b\xc2\xca\xf0\x91I\xb6\xba\xff\x04R2\xd0\rJ\xc9@Uh\xecD\xc7\x93\x81\xf6\x08T\t&\x02\xd8\xaf\xba\xff?\xa8\xb8\xffw\xaf\x90H\xe9U97\x0c~\xd8\xbf;\xad\x8eb\xa5\x1b<D\xad_<\xeeUG\xc3\x91v\x80a\xa3\x9dM\x07\x9e\xb5D\xc9\xbbP\xd9\xd3\x81\x1f?\xfb\x8c\x0cx\xb2\\8\x14\xcb\x82i\xa6\x03g\x06\x9b\x07@\xa9\xdc7\x1au\xa2\xff\x9e\xea\x1e\x19\xf6\x02\x95=2\xdcwP\xfd\xbdQ\xdc\x02\xe7\x84\x8f\xbbvmk\xe3\x8ftq.Z\xadl\xe3\xc0\xb3\x80\x81S\xe5\xd9u\xec\xd2\xdb\xf1\x82 {|T\x10\xe4\x91\xc7\xce\xff\xa4 \xc8\x87\xde.\x08\xb2u\x97zA\x90LG\x0b\x82@\x13N\t6\x02x[e\x1f\x8b\x0e\xbc:\x06\xc0\xa4\x9b\xd4\xca:\xc1\xcf\x0fW\x9f\xb7JLa/\n\xa3\x97\xca\xbd\x8c\x1a;Y\xcb\x10\x88\x8aE*\xc5B\xbcR\x12l:J\x82}\xee\xb5\x95\x1f\x89=\x93\xa6$\xff\xb4$\xd8t\xff)\t\x06\xa1v\xb8$\xd8\x9f\x8d\xd2{?V\xeaaY\xfc\xa3V\xad\xda\xb2\r\xb7\x9a\x91\xec,\xed=|ZF\x0c\xaa\xfc\x88\x08\xf2\xf1\xe6\x8a\x82\xf2U\xe8\x9c\xa3r/\xc8\xf6C\xd4\xa2Jd \x9e\xc5\x8a\xb5\xb9\xb2\xe1\x87\x8a+\xd0\xe9\xa2\xa0-\xbcZ\x14\xf45\xea\xdb\xcf\xa2(\xe8+^*\nz\xeeY\x8aS,\n:T\x16\x05\xb5\xdeZ\xcd\xbfc\xbdj\xda9\x8a\x82\x06]\x93PK\x0f\x002\xe02s\n\x94\n\x7f`\x05E\xb1N\xd4\xebS\t\xefE4\x9f7UY\x9c\x1b\xea\xb2\x92O\xb9u{q\xef\'\xd5\x0c\x9d\xe2Yd\xe6\xec\xa1\xba\n*;\xac\xcf\xde(\x0b\xbe1;\xb7\xe2\xca\x82\xaf\xc9\xf0RY\xf0\x0c\x87\xcb\x82\x17\xd3X\xf5\xb2\xe0/\t\x84\x07\x1b\x01XV\xfeE8k\xce\xf6"e\x0f\x00\xaa\xf7\xaaD\xcaEF6\xa0G~v\xce\xab\x1a\x00\xce\x8d\xb0a\xe4\x0eX\xc6\xd9\x8b{F\xb5a\xd5\xef\x99\xb3\xadH>\x1b\x95\xd5\xaa\xef\xa0$\xb5\xc6 \x1b\x0b\xa8a\x8cZ5\xe2\x1e\xdeh\x0c\xf2:\x1a\x83t\xb5ns\xde\xd7[\x8dA:)6\x06ia\x19\x02\xecj\x0cr\x9c\xba\xf7\x1e\xa4j\x00\xdco\x04a90\xcb\xb6V0\xb6\xe4\xee\xbaWY0Py\x07\x95{U|\xffOy\xd9\x9a\x8ds?\xf9\xcc\xcbJ1\x01\xb8g\xd5\x0cA\x19\x12,\x9e\x89J,\x80!\x1b\xa6\xb4\xa4\x8c\xcd\xce\xb6\x06C\xf2\xcd\x16o\xb4\x06\x8b\r\x80\xd6`\xc3ov\xba5\x18\xe4`\xa1\x11\x84\xa3\x82\t\xe0\xe5\xa0 \x00\xd9\x1ct\x89\xf3\xcdA\xd1\xc6\xcb\xd9\xe6\xa0oQ\xcbV\xd6\x86\xc8N\x9d\xbb\xd2+B[p\xae9\xe8\x8bZ\xcdAU\x9f%\xb6\t\xd5\xd5\x9b\x83\xf6\x0bF\x02\xf8\x07o\x01\xecm\x01\xb25\xb6\x002\x80g\xd4$\xaf\xb4\x07_t\xfb2G\xdb\x83OTi\x0f>+\xd5\x11/\x84l\x0f\xfe>\xda\x83\xcfS~\x8e\x89\x9dz\xca\xf6\xe0\xb9\xce\xb6\x07\x7f+\xd8\x92\x80\x82\xc8\x08X\xe8\x15#`\x86\xa2\x11\xf0jBL\xcbv\xb4>\xb7H\x81\x04\x8aibr\x9ar\x89\xf4\x86\xd1\xd1t\xe4\xbe\x07\x1c\x0b\xa3>\xf1\xe0#\xe5\xb6\xe7\x82\x07\xe2\xe1G\xcf:v\xbd\xbd\x07\x0eSxx\x84\xd2w\x85\xdbu\xda\xac\xa5\x96\xab\xbf;\xc3\x12MD\x15\x7f\x9f\x02#H\xcb\x81;\xef\x06<\x12\x1cn\xc0\xe5k\xb7(\xb9\x01\x8d\x12\xd5\x89\xe7,\\\xab4ya\xe0j\xd6\xa2\x8d\xf2\xb9\xbbu\xef\xe1\x98=\x05\xda\x04H\xb3u\x9b\xb6\xd7X\xcfa\x9dO\xec\xd0Qf\xf59\xd9\x0b\xb0}b\x07\xe5\xef\x89v`\xebs\x0f+EVN\x9fs\xa7jS\x17\x18\xc2o5\x82t\\\xf2N \xd0d\xc5@\xa0\x1bd\xb0N \x06\x02!rP\xb7kP\x9f\x01#\xa5\xa1\xcf*\x81\x05\x13\x1c\t,*\xd1\x94n\x8c\x9f0Y\x86?;e\x0f@U\x9eu\x19\x9b\xe8\xd6i\xb7Q\xf2\xf4\x99\xb4~\xe3fI2N\xed\xfb\xe1\xc1H\x1a\xa5\xac\xa2K\xa3\xe7\xb4\xd9\xcb(\xcf\x82@\xa5\xf5\x7f\xc7q\xea\xd6k\x80\xea\xb9?\rF\xff\xbfV(0\xc2^uB\x81\xe7.Z\xa5\xe4\xcf\xf6\x97P\xe0j\xba\xa1\xc0\xe2\xb8\x89\xb7\xce\xd1\xaeB\x14\xd9 \x9a\xee\\\xbb\xdd2(\xc8m\x0bPI\x11.\x19\x1b\x80\xbd\xf4[\xef|\xe4\x98\x90\xe2\x19\xa2\t)p5\x1f\xc0\x81\xf3\xbe\xf1\xf6\xfb\x94,\x88E\xc5\xe7\x7f5\xa4\xbak\x1f\xb9\xf7\xb7\xdcB\t\x82@\xe0\x95J\x895\x13\x85\x02U\x83\x95\x00\xf6*\xb9]\x86\x8dV.\x06\xe2J\x06:\xa8\x9c\x0c\x84J>\xdeK\x06\x1a\xe6\xbdd\xa0\xa1\xa3\xb5\t\x00@\x0b0\xab\x15\xcc=\x91S\x17\xadS\xaddc6l\xa9!\xd3\x85/\xbd\xf3\xa1\xd7\x93\x85\xec\x0b\xff\x074\'5M\x92\xae\xea\xf7\xaaW?\x92\x16,\xdb\xa4\xb4\xfa\xc3\xf8\x077\xa1\xe2\xb9\xff.0\xc1\x08\xe2\xa1\x96\x0e\xdcN=\x1d\xf8\xd0\xd5\xe2\x99:\xe9\xc0\x1b\x9c\x9dl\x1f\xe9\xa7\x03#\x84\xd9\xe9t\xe0\xd2\x10\x1b\xd7\x94Vo\xd8c\xb9\x92\xb9\xeb\x04\x0c\x1e>N\xab\xaa\x12T\xe5\x94\xd9s\xe9\xe2\x9b\xef\xfa\x15\t\xb8\xd5~l\'t\x84\x1fZ\x02H\xd3\xca\xef\xef6\xa0\xa2\xfe_\x83(\xe5\xaaP\xc8\x85\x89\rf\x02\x18e\xa8\x16\x04\xc9;\xa0W\x10d\xde2eK\xb6\xab \xc8\x11\x87\xf6\xaf\xbf\x95\xaa?\xac\xe3*\xd7\xc6=\xce\xd2,\x08\xb2Q\x16\x04\x89\xb4E\x00\x10\xe6\xa4\x9b\x93\xd5\xb4\x003\x98%\xa1u\x07\xadk`;0\xee\x96\x89\xf4\xe4\x85\x97*\x9c\x04\xdci\xc5g\x9f|\x9eF\x8d\x1e\xab\xa5\xf6\x03m\x13\xbbZ&S\x95\\\xfd\x87\x8c\x1c\xafs\xfeL#\xc8\x07\x8c\x1f\x8a%\xc1Vz\xb5$\x18\xf2\xdc\xf7:P\x12\x0c6\x85&:%\xc1\x9a\xdb-\tf\xbf\x93qtLcZ\x9e\xbe\xd3\xd2\x16\xe0^\xd5\x10\xf8\x12\xae\xb8\xa5*\x89.]\xbb\xc9\x1a\x82\xd8\xc3W\x04\x11\xe0\x9a\xa8\x08\x84\xdf\x04\x1e\x04\xdd\xfb\x8fj\xd8\x88\x16\xaf\xc8Q{N\x05\xae\xe2\x9f\x11\x91\rU\xcf\x8f\xe4\x9fN\xc1N\x00\xcaEAu\xec\x00n\x12@\x1d\x01\x9d\xce\xbf\x88\xd8\x83\xea\x8e\xfd\xbbnQP|\x06\x9fm\xa8Q\x14\x14\xab\xd1\x94\xe9\xf3\xb4\x8b\x82\x0eT,\nZ\x1e\x10\xa4\xa2\xe2\x11pc\xe2\xb44\xe5\x08\xc1k\x84(\xaa\xa1\xb4\x0b\\0\x0b\x80\xfa\xa6"\x90\xabr34\x909s\xd3(\xc2\x86\xb6T\xb3V\x1dY$Ee\xe5\x07\xb2w\x1c\xa7\xde\xfd\x86\xe9\\\xe3P0\x1b\xffJ\x8e\r*\x0f\xccNYp\x94\xdc\xd6m\x07\x86};*\xf9@\x1b\x80\x1b\xaf\xbc\xb2\xe0\x1f\x98e\xc1q,\x0c~\xbae\xc1\x11\xfc\xa3]\x16|\xd7\xbd\xd4(\xae\x89\xc7\x04\x80 "\xa4\xaa\xaa\x18\xb6\x90\xf6\x8a\xc4\x96\x11\xa3\'S\xa8\r\xcd\x03\xdb\x0e\xf4\xe6Ck.\x84\xfb\xba\x9f\xa17V|\xfc&\xcf\xbf\xfc&m\xd8\xb4E\xcb\xc7\x7f\xbd\xeby\xf4\xb8\xe9\xca\x04\t\raV\xdaj\x9d\xb8\x8c\xff\x11\x18\xc8\xa2\xff\xa3\x1d@\xa91H\xaa\xdd\xc6 6\xba\xf8\xc0}\x07\x1f>\x02y\x90\xd2+\x1b\x83<\xf3\xb2\x04^#X\x05\xef\xe1\x18\x15W\x9fQJ\xc5\xde44\x069\xa1\xd9\x18d\xc1J-\xff\xbc\xd5\xfe6S!:\xb0d\xf5\xe0~\x83\x92\xb4\xf7\xd1%\xdd\x9d]\xbb\xf5\xa0\xcc\r92\xfe\x1e\xc5B\xdd\xe4jw\xdb\xe5&c\x84\xf4\x9e}\xea\x05i\xd0\xed\xd4\xb9\x8b\xedg\x04\x9b\xcc\xe0\x11\xe3d\x15%\xd5\xe7\x82\xa8\xbf\x16\xad\xda\xeb\\\xe7\x88@u\x16}\xd7@+\xa4\xcb*\x0f\xae\x87Y<S]e>+\xdboy\xde\x1a\xac\xa6\x8c\xe7\xbf\xb65XM\x0f\x84\xcfl\rv\x8fw[\x83YO\xf6P\xb9\xd2\xa9X\xb8K\xc6\x07\xf4\xe9?\xdc6\t\xb8\x8d\x84\xb0\x93\xa0\xea\x0fJ~\x81\x0c\xde\xfc\xf9\x87R\xa0Q\x96\xbb4\x8d\xab\xa4\xe6\x85cp\xec\x9bo\x7f \x8d{\xdbv\x16\xc8s\xa1\x1c\xbbj%\xe8\xb2\x84\xbf\xff\x90\xd1\x96\x95~\xae\xcf\xa0\x1c\x964Qg\xab\xf9{\x81\xfe,\xf6?\x0e\xbd\xe6\xa0\xe9\xf6\x9a\x83v\xf4\xa3\xe6\xa0\xb8\x17[\xcdA\xd7\xe5Q\x1d\r\xbf\xbc\x9a\x8f;\x82\xe6\xdd\x9e\xa1\xb8\x15\xf8\x91\x04P=\xc8\tM\x04%\xbfP\x85\x07[\xa8\xb9\xf3\x17\xca\x88\xbf\x03\x85\xf7\xd2\xa9G\xce\xc8\x15\xfd\xc2\xf3\xafI\xfb\x01\x04\xbd\xf8\xe1\xc7\xa5A/cC\xb6\xdc\xdb\x0f\x188D\xb6\x17C\xfc\x81\xa7\xf7\x01\r\x13+\xffF\x85`\x9f\x92\xaa\x7f\xca\xfc\xd5B\x03\xac\xabs\xad}\x02\xd5X\xec\xaf\x1d7\x19\x8a\xed\xc1\x07\x0cI\x92\xad\xb2\xf5\xda\x83\x9f\xa3\x8d\xb9\xfb\xa9\xa5\x9e\x9a\xe6\xb5\xf6\xe0\x1b5\\\x9a\xd7\xb6\x07\xbfQ\xf5:H\xb3\xfe\xde\xd0H\x14B\x83P\xf5\x89\x7fRF\xc5\x8d\x1c3\xd5\x96a\xd0\xca0\x8a-\x15\x0cwQ\r\xa3e\x85^ \xaaaC\n\x8f\x88\x90\xb9!\x9eh\x1fF\x19\xe9\xd2Ic\x93)k\xdb}Z\xc2\xbf"}\xa7l\x0f\xa6q-\x84\xfdv`q\xff\xe9h \xf0\xaa\x92\xf1\xaa^}\xd9&[G\x0bp\x93@z\xd6\xdd\xd2\xf0V\x91\xc2\x9f\x9e\xb5[[\xf8]\xad\xc1\xf3\xe4wW\xbc\x16\x9e\xe5\xdd\x86B\xbd\x85\xab\xdb\xab>C4W?\x97ap\xd2\xf4\x05:\xae/\xbf\x03\nv\xde\x9ar\x87\x0cz\xd2\xf9\xeeH\n\xea\xdc\xad\xaf\xce\xb5\xfe-\xb0\x82E\xbd\xec\xb1Z\xe0\xbf*\x0f\x13\x99s{\x8a\x1e\xd6R\xa1K\x06\xd1@\x05\xf7\xc4&\xa0\rq-\\\x13Z\x88\xae\xf0\xe3;\xe2\xbb\xaaf8\n\xfcG`\x99\x19a\xf6\xb2\xce\xbe\x1c\x11o\x10jUAp\x17\xc5L[\xba\x91Z\xb6\xe9\xe0\xdbg\xea\x80\xa6\xd1\xb6}WZ\xb4<G\xe3\xfb\xba\x84\x1f\xed\xc0\x10!\x19\x12\xa2eo\xb8`\x04i\xce\xbf\xeah\xa3\x12\x14$\xf7\x8d5\xc2d`\x90.\x01\x94\xb4\t\x8c\x185\xde\x96w@\xdf\xda_\x93\x86\xdd8\xce\xdc\xf3\x9f\xb3u\xbfs\xd2VPu\xf5}.\x9eak\xf3\x99\x8eS\x89\xb4\xfcq?^\x93&\xdc:O\xd9(XR\x1d^\x97\xbd_F\xc1\xd5\xd1\xa8QPQ\xa8[/B\xba4]\x11~\xc5\x1a\xdf\xf5\xa44\xfa\xdd4a\xa6\x0cy\xd6\xb8\xe6\xd7\x02CY\xc4\xad\x8d\x81y\xea\x91{\t\x94\xbd\xb5P\xcb\x8dVR\xa8`\x81\x87\x1b\xaee\xebD\xc7\xf7\x94\xee\x15&\xa1e[y\x8d\xbdG\x1e\xb5GV\xe2\xbbem=D\xf1M[\xe8\\{\xb3\xf1c{)\x18\x9b\xf2M\xad@\xe9\xf3\x10`\xa8\xc4:\x04\xe0^\x19!\x1cs\x17gP\xbb\x0e\xdd\x95\xb21}\r\x08-\x1a\xa5@c\x01\xc9\xe9\xac\xfc\xeeP\xdfI\xd3\xd2d\x90\x90\xc6u\xb1\r[o\x04i\xc1\x0f\xdd\xd1Q\xe0W\xaa\x0f\xb7\xdf\xa0\x91\xb6\xb6\x02n\x17!\xf6\xd6\x08\xc4A\x8b\xeef\xcd[)\xe7\x0eX\xb9\x92@N8\xa7+\xc8\xe7\x9cR\x92OY\xaa\x7f\xdf\x81#t\xae\xff\xb9@b)n\xd6g\xf5<\x03\x914c\xce\x9d\xda$\xe0\x0e\x89\xdd\x90w\x84\xa6\xccX$}\xe3N\xc5,x\x02\x04\xf6 \x9f!9e\x89\xcb\xceQP\xac\xf9\xbdNJ\xe1\x9fz\xdbb;^\x98\'X\xf5W\x1fX\xb9\xb2t~\xd8)3\xe6\xd3\xc1\xa3O\xd8 \x80\x1f\x05\xcd\x9d;\x80\x04"\xf8\xd9\x91\x9e\xabSl\x03\xfbg|\x06\x9f\xc59p.\x10\x8c=br\x01\xdfi\xf2\xf4y:\xf7\x01\xfb\xc9&\xa3\xf4\xe6\x92\x03\x0c\x85\xeaK\xd7\x93\x00\x04Fn\x074WJ\xac\xac\x102T"\x9e,\x88\x00]t|\xb1\xdd*-\xd8\xaa]\x87nR\xa3\xc9\xdcR$\xd5\xfd<\x1b\xdf\x05\x9a\rV~\x1b\xc2\xff\xa1@7\x16k\xbd\x91 \xf0\x0b\xe5\x89Z/\x9c\x16.M\xf7H\xd8\xdcD\x00\x8d\x00i\xb9P\xbbQ\x85(i\xecdip\x84\xe7\x00E;Q\xb9\x17\xc0k\xfc\x0f\xef\xe1\x18$\xe7\xc0\xc0\x87\xcf\xe2\x1cN\xdc\x0b\xbeS]\xf1\xdd4&\x1bRK\x9b\x95\xf3\\\xd1w\xee\x1b\x9d\t\x8c\xed\xc0\xf8\xa9\xf34\r\x83?%\x82\r\xf9Gdm\x01\xf4\'@\x99\xecj\x9a!\xd3\xbaj~\xa3\xb8\xa62\xa0g\xee\xe2t\xb9\xe2\xa3D\x97\xdd\xfb\xcf\xdeq\x8c\xc6NH\xd1U\xfb\xc9\xb4\xbdLaq\xb67R\r\x85\xa6!nD\xc7\xc6\xc9 \x19;\xf6\x80\xd2\xea\t@mG\xd6\x1d\x04\x11u\xfaP\xac\x13\x15{\xf3\xf7\x1c\x93\xc0k\xfc\x0f\xef\xb9\x88\xe3\xbcmU\xbf\xb4}?j F+6\xe80\x81\xea\xca\xb3-\x9e)\xec\x019\xa6;J#P\xa7&\x8d\x18=\xc5\x8c\x8e+\xb6\xb7-\x10\x82\x04!\xdc"V\xd25\x9b\xf6\xd1\x8c\xd4\xe52\x19\xa9E\xcb\xf6\xd2 \xe7\t!@\xe0\xa1\xad@\xc5\x1f4|\x1c\xcd\x9c\xb7\x8a\xd6e\xed\x97\x9a\x8b]\xc1w\x1b6\xe1\xeaCp\x90\xa6\xc1\xcf]\xe7o\xad\xc1\xc9>\xb6\x07\xb2\x04\x8bu\x1ez|\x93\xe6t\xd7\xfa\xed\xce\x90\xc0u\xb6\x02\xf76\xe1z\xa8\x86\xf1\xea\x08\xff\xea\xccm\xd4\xb8Is\xdd\t\xf7\x80\xf9\xcc\xacF\xb8\xc0\xbd\xaa\xee\xd6\xabv\r\xb1\xc5\xe9\xd1g\xb0\xab\x90H\x81=\x12\xb8\x9e\x0c\xf0\x1a\x11\x85(Q\x06B\x18u\xf34\xbaa\xc0H\xea\xd0\xb9\x175Oh+\x0b\x97\xa0\xb0FxD\x94\x04^\xe3\x7f\x08Z\xea\xd0\xb97\xf5\x1d\x98D\xa3o\x99A\xb7\xcd]A\xcb\xd3wH-\xc3]\x90\xd3\xae\xd0_\x1f\xe4\xd3\xb9{_]W\x9f\xdb\r\x8b\xc8\xd6\xda,\xc6\x9e\x8d\xaef\xe4\x94\x16\tHM\xe0\xf8Y\x87I\xc0\xfb\xc0=c\xe5\xb7!\xfc\x1f\x0bt\xd6x\xae0\n>fg\xb5m&\x04\x13j\xb5\x1d\x0bz\x99[\x04\x93\x10\xd0\xbb\x10\xe7E4\x1eV\xde\xf4\xcd\x87\xa4kqm\xd6>\t$\xdc\xc0m\x07\xd2\xc8\xdav\xd4\\\xe1O]\x15x\xa7\xee\x07\xfb}d\xf6\xa1\x9b\x92M\xad\xa4\x98\x8d~\xce\x8d9\x86b\x88p\xc9\xed\xc0\xc2\xa5\x19\xd2\x88\x16\x08D\x80{\xc4\xbdb\xcf\xaf\xa9\xf6\x03\x7fUP\xfdK\x1b\xad\x04\x9e\xb1\xe7C\x0f\x97a\xb3\xb2\xd5\x98\x87\xda@Y\x16w\xb7@\x97\x05\xab\xae\xbcv\x00"A9t4P\xa9m?\xdf\x02\xc4\xda\x84\xc5\xd6\xb9QC`\xa7\x8e\x1f\xdb=IQhC\xba\x08\x1d\xdf\x128\xab\xf2\xe3\x1eq\xaf\x9a\x06?\xb7\xaa\xb9\xcd|FvF[]\xf7\xe0\x8f1\x0e\xa1\xd4\xbam\'\xe9\xf3w\x85\xd0z\x83\x08|\x03\xdc;\x8c\x9c\xb3\x17\xac\xa1\x96\xad;x\x12\x13rV\xa09\x8b\xac\xf3#\xc6\x8e\xca\n\xf7\x19\xe2\x04\xb2\xb7\x1e*\xb1g\xf7\x9fU\x1f\x80\xb7\xa1\xdf\xc0\x11\xda\xf5\xfdM\xfc\xcc\x01U\xb3\x9d]M\x00\xc0J\xd9\x7f\xf0hY\x08\xd3\xadB\x07\x92\xe0\xe7\x8am\xc4\xd2\xbb\xf2eC\xd4Z\xfaV\xfe\xeb}\xfd\t,\xaa\xde\x1b\x98\xa8\x17\xed\xfc8\x08\xcaA\x11\r\xac\xb4E~\xa0\r\x14\x99\xab>\xc2{5#\xfcJ\xe2\x15s\x05wb\xb44\xc9\xe4\xbfv\x05 *\xba\x91\xcc\x0c\\\x95\xb9\xfbG\xe1\xf2W\xc1\x97\xdb\x96\x07\xa4\xe1p\xe8\x8d\x13d\xaf\x04\x0f\x04\xff?\xa6\x016\x9eE\xd4\xfb\xa3\x8f\xc0\xbbv~(\xe4\x0e\xc0g\x8f,B\xa4\xd5:\xe1\xab\xb7\x13c\xb0O\\\x1bY}H\xec\xa9n?\x87\x1d\xcf\xa0\x97\xc3\xcf\xb6\x91\xe9\x1d\xf8\xb7]a@"Ptl\xbc\xdcC/[\xb3Un\r\x9c\xb0\xc8;\xb3\xda\xbb\x0c\x8dP\xf5\xefX\x9dKCF\xde"I\xcb\xc3\x98\x03\xa4[\x1f`\x83\x9fo\xc7`\xc3\x15]e3\t\xa4>\r\x18\x9c$\x89\x00\xd5u\xbcM\x04n\xc1\xc7\xb5 \xf8\xc8\xe7\xd7H\xe9-\r\xef\x0b\x0c\xf2\xd2\xb3\x85\x8b0[\xe0/\x9e\x06\xe3\xa0\x82p\xaf\xbe\xc3\xa45=cK\xa1c\xee9\xbb\xee\xc6\xf4\x9cC\xd2]\xd8\xa3\xf7`\xad\x8e\xcaF\xf9\xed\xbc\xe1\xe7\xaf\xc3"\xe9\xfb1\xc8\xae&\xe0\x06B:\x11\xb6\x8b\x8cB\x14\xd9D\xa5]w0\x8f\'\x84PX"\x88\x08\xe7\xc4\xb9\xb1\xfd\xc0\xb5\x1c\xa8\xe4\x83\xef<\xc0\xcb\xcf\x16u\xeaf\x19\x9aa\xc3\xe5i^M\x9b\xb7\x16\xaa\xf6x\x9a{{\x86\xb4\xb2\xc3\xcd\x06\xf7]\x9e\x9b\x10\x1ct\'\xe6\x99\xeeDh\x1fp\x1b\xceY\xb4V\xa6\xed\xc2\xa5g#\x98\xa7\xbc\xa2\x1eS\x05BY\x14+n\xf46\x14\x0b\x88\x18\x16\xfd\x06Paw\xd0\xd0Q\xaep\xde\xbc\x03\xb2\xeb\x8e$\x84\xfb\xcfKA\x96Z\x82\xa9)\\\x83\x13\xe7\xe4{\xf2\x98\xfb]\x02\xbfK|\x16\xe7\xc0\xb9P\xba\x1b\xe7v(\x19\x06y\xfd=}\xf8|\xfb\n<\xe5\xc9\x96\xc0(%.\x1f\xed\xb2{\xf7\x1b.S\x8e\x17-\xcf\x96B\xbai\xdb}\xa6\x86p\xca\x8c\x07(6\xc9\xa1\xb8\x14\x17`\xb1)\xe4\xc5\xd7\xc4\x0e\xa0:\x11\xce\x85\xf6]\xb7LI\xa5^7\x0c\x95AC\x0eW+\xfa\x97i\x8c\xee\xce\xe2W\xb1#\xd4T\xbd\x06\xd95\x0c\x96E\x06\xe8@\x846d\xe8A\x80\x86\xa4\xf3\x16\xaf\xa6\x15ks)3\xa7\x80r\xb6\x15\xc9\x15\x1d\xc8\x16\xaf\xf1?\xbc7o\xd1jq\xec\x1c\xf9\x99\xd6\xed:\xca\x8e=\x9e4\xed(\x05\xaf\x0b\x0c3\xf7\xe9\xf1>@c\xf3Z \x9c\x13\xe6\xc4w<U\xbaV\xed:2/\xa0}\xc7\x1e\xd2\x930\xfa\x96\xe94u\xe6\xed\xb2\x859\xc8\xe1\xce\xb5\xdb\xa4Q\xf1\xae\x8d\x05\x12+\xc5\xebe\xe2\x7fxo\xf6\xc2523o\xd4\xb8\xe92\xbf\xa0]b7j\x18\x13\'K{U\xf1Bj\xb7\xb9\xdf?,\xd0\xa5\x94\xdf!N Z\xa0>k\x05\xde\x1ba\x86+\xdam\x81\xe1j\xa8\x00\xd7\xd5e\x81?\x18^N#\xc5\xa4B\r}\xec\x1dA\x10\x00^\xe3\x7fx\xcf\xa6\x0bO\x07\xdf\x08|)p\xc5\xc7@\xe7\x9a\xdf\xeb\xc6`xJ\xc2X\xb5A\x0eHDB\x9e\x00\xe2\xfc\x01\xc4I\xe0\x7fx\x0f\xc7\x84:K\xb2*9\xfd\xff\xaf\x8c\xdf\xe1\x0b\xd36\x839y\xd0\x9c\xa3\x9d\xcc9\xcb\xc3\xc3Q\xcbp\xf5\r\x80\xab\xe5+C\xa3\xc6\x1d\x83QA\xf8\xc1\x9c\xab\x0f\n\x8c58\'\xc0\xf6\xe8i>\xc4oxR1\x02\x14\x7f1\x17\xaf\x9e,\xcez\x96h\xa4\x03\x7f\xce\x13\x88QI\xf0+sN\xd7`\xf1.\x7f\xd4\x14H7\x14Z\x851\x18\x01\x06\xcc\xe9\r\xe6\xb6\x96G\x19+?\xfa\xa5\xff\x83\'\x0b\xa3\x92\xe2;s\x8eW\x96\xbe\x80\xa8A\x81\xf2\xf3\xcdM\xe0u=\xbb\'K\xe5\x95\x9f\x11$\x9a@j\x00\x0b=\x04|\x84@\xae\xc0y\xc3U\x8f\xe2+\x13\x9f\x98\xf1#\xa8D\x9dd\xb8\xa2K\x95F/\xde\xf33\x82\xcc&\x10h\x86Al]n\x118\xa3h\x98\x87\x01\xf4i\x81\xc9\xe6\xd6\xbe\xccQ\xdb\xb4\xf6\xf3\xc4`\x04\x13\x1e\x08\x10\x17a\x15s\x81>f\xd8\xcb\x13AA\x9f"\xa3\x9c\x82\xb5c\xed\x9c8,\xac\x96\x0c\x0eAP\x0e\x83QQ\xc0\x1c\xc4\\\xb4\xe9"\xbc\xc9\xcf\x85\xbf\xa9i\xb8\xfc\x8d\x03\x84\x87@\xa9\xc4\xd2\xac\xfe\x0f\xe8\x9c(\xc6L9E5\x9a\x15\x19\xbbd\x95Y\x06\xa3\xa2\x809\x88\xb9\x889\x89\xb9iC\x0b\xf0\xc7\x88A\x18\xf7PF\xfe\x92\xe1A\x9d\x882H\xa0\xf9\xf5\xc1>_\xaa|\x18e\xa8\xba\xf5\x1a(\x1f\xb8;\xd5\xd3\xaav\x1c\x83\xe1\x0b\xb8\xe7\xe2\x8a\x8c\x9dr\x8ejT\x12F(q\'?\x12|\x941G\x8e\xcdi/z\xe3\x8aJ\xbaBW\x19\x8a\xc9&x\xb0\xa8\x16\xeb\x9dB\x94\x0c\x863\xd5\x860G\xbb\x8b\xb9\xaa\x116\x9c\xe6\'\xc2\x8f\xcaP\xa81\xf9{/\xdb>`\x13\xb8\xda0\xe5aU\xb5_\xae\xfc,\xfc\x0c?\x07\xb4\x01h\x02\x1a\xdb\x01$\x10Ud\x16a\xa4\xc0"\x81\xf7|h\x00}\xca\xbc\xae\xdaE\xb1\xbf\n\xa4\x82\x93\x8c \xd7\x04\xc4\\\xc5\x9cU\x14\x86\x0b\x9e\x04\xcfx\x18x\x87D\xbb\'\x05\xfe\xe9c\x0f\xc8\x9f\x05n\xc6M\xfcI\xc5\xda\x8fj2\xf9\xbc\xfa3\x02H\x0b@\x03\x15E\xef\x00\x16\xc1h\x1f\x0b?\xbap\x1fP\x91?+\x84V\xadF\xf5\x1b4\xa2\xfaQ\x8d\xc4k\xad\xd4\xf8}\x86\n\xf3\xc0\xcd\xe26\xfc\xf1\xe4b\x04\x8a\x06\x80m\x80b\xaf\x07\xd4\x13\x88\xf3\x91\xe0\xc7\x98v\xb7\xcf\x9cX\xc9\xe3\x12:P\xf2\xf2=\xb4\xf9\xd4g\xb4\xe5\xa1\xcf(\xf9\xce\xbb)<J\xb9\xb9\r\n\xddX\x1f\x08_+\xdc-L\x00\x8c@"\x00\xccY\xc5\x02\xa4\xf0\x04x\xbb\xac8\xdc\xed\x13\x05^2\x1c(\xf3V/"\x9aF&\xaf\xa0\xcd\xc5\x9f\xd2\x91\xd7\x89\x8e\xbcAt\x8f\x00^O]\xbaKj\x05\n\xe7\xf9=\x13\x00\x83\t\xc0\xbb\x04P\xc5t\xb5\x1fs"\xcf\xa6Z\xf50\xea6h<\xad\xda\xf7\x02\x15\xbe\xf2o)\xf8\x87/\xfe\x08\x90@\xce\xc9\x8f\xa9^d\x8cj\x995&\x00\x06\x13\x80\x97\x08\x00=\n\xd7;\x11\xc5\x87\x9e\x0fM\xdbv\xa7Y\xeb\x8eP\xc1\x85o\xa4\xa0\x97\x14|7\xa0\x01l{\xfc\nED+{@\x98\x00\x18L\x00\x0e\x13\x00\n\xe6N\x17x\xc3p\xa0\x9ecx\xc38\x1a3+\x9d\xf2O\xffZ\xae\xf8\x10\xf2\xd2\x84\xff*\x01<\xc6\x04\xc0`\x02\xa8\x08\x02@,\x01\xfaF<$\xf07O\x05\xbfF\xcd:\xd4{\xe44Z[x\x91\n_\xfd\xe1\'\xea>\x13\x00\xc3\xaf\x05\xb0\xf4\xb6\xe2\x95\x96\x00\x10\xc5\x97\'\xf0\xb5\xa7\x82\x8f0\xe6V\x9d\xfbSZv1\xed{\xeeoe\xaa\xfbL\x00\x0c\xbf\xeb\xf6\x0b\xff;:\x0fm\xc8\xbfGv!Z\x9b\xb5_\x02\xaf\xf1?WW\xa2b\xaf7/\xf5!\x01D\x98\xa1\xc4\xef:\xe1\xd6\x8b\x8aK\xa0\x89\x8b\xf2h\xfb\x13\xbf\xb3T\xf7\x99\x00\x18\x15\x0f3\x11\'{\xfb1\xd9\xe6{\xfc\xd4\xb9\xb2\xf3P\xab6\x1d)\xa6Q\x13\x8a\x88l(\x81\xd7\xf8\x1f\xde\xc3186{\xc71Wp\x99\x17\xe6\x95\x0f\x08\x00Q|7\n\x9c5\xad\xe9\x1e\t~\xad\xba\x114p\xdc<Z\x7f\xf4\x9d\xab\x82\xac#\xf8L\x00\x8c\nY\xf1\xd1V,e\xfej\xea\xd2\xa3\x9fl\x1e\x12\xa2\xd0\x15\x08\xc7\xe0\xd8.\xdd\xfb\x89\xcf\xae\x92\xe7pZ#\xf02\x01\xc0\xba\xbfG\xe0\x8fND\xf1%\xf6\x1eIKw\x9c\xa5\x83/~\xaf\xa5\xee3\x010*\x08\xaey\xb0x\xc5f)\xc4\x9e\xf4\xff\xc3gA\x1e8W\xc9sW\x00\x01\xa8F\x02"d\xf8QG\xa2\xf8Z$\xd2\xb4\xe5\x05\xb4\xfb\xfc\x1f\\\x82\xff\xbag\xc2\xcf\x04\xc0\xf0\x89q-g\xc7q\x9a8-\x8d"\xa3b\x1cKN\x89l\x10M\x13\x93\xd3\xc4\xb6\xe0\xb8#\xf3L\x93\x00\xbe6Kn\xc5\x19\xe5\xf7l\xc4\xfb\x99\x9e\xba\xf6\xea\x84G\xd1\xf0\xa9K)\xa7\xf8\x13W\x14\x9f\x03\x82\xcf\x04\xc0\xf0\x89\xf0gm?J7\xde4U\xb6\x1dw:C\r\xe7\x1c1z2em;\xea\xf1\\\xd3$\x80\x1fL\x12P\xe9\xd7\xf87O\xa2\xf8\xba\x0c\x1cG+\xf7>G\x87^\xfe\x97\x92[\x8f\t\x80\xe17j?V\xfe\x91c\xa6x\xb5\x19k\xd5j\xd5h\x84\xb8\x06\xae\xe5\xc9v@\x93\x00\xbc\nD\xf15i\xd3\x8dR\xd6\x1e\xa6\x82\x0b\x7f\xf6x\x9f\xcf\x04\xc0\xa8\x10L\x12j\xbf7V\xfe\xd24\x01l1|\xa8\x01x\r\xc8\xccC\x14_\xde\xe9/\x1cW\xf7\x99\x00\x18>\xb3\xf6\xc3H\xe7\xe4\x9e_\xc5&\xb0x\xe5f\xdb\xde\x81\x8a&\x00D\xf1\xf5\x1a\x91Lk\x0e\xbd\xaa\x1c\xc5\xc7\x04\xc0\xf0K??\xdct\xb0\xf6\xfbZ\x88\xe0\x1d\xc0\xb5\xed\xc4\tT$\x01\x84\xd5\xaeG\xb33\xee\xa5\xfd\xcf\xff\xdd\xab\xea>\x13\x00\xc3\'\x95u\xe0\xe7\xb7\xe3\xea\xabW\xa3\x06\xc5\xd6\xae#\x81\xd7v\\\x84)i\xabmU\xa2\xaaH\x02\x80\xf0\xed8\xf3\xb5\xcf\x85\x9f\t\x80\xe18\x10\xe1\xa7\xbb\xfa\'6hH\x19\xfd\x86\xd0\xb9))\xf4n\xea\x1d\x12x\x8d\xff\xb5\x17\xef\xe9i\x01\xfde\xc4`\xa0\x11\x00\x84\xd0\xdb\xfb}&\x00\x86\xd7\xf7\xfe\x08\xd9E\xd4\x9e\x92\x05?$\x84\xa6\'v\x91\x02\xff\x8fU\x9b\xe8\xfbUY\xf4\x9d\xf8\xfb\x9d\xf9\x1a\xff\xbb,\xde\xc31U\x15"\x06\xddso\xe9\x9a\xad\xda\xb6\x00&\x00&\x00\x86\x03\xea?\xe2\xf6C\x14\x85\x15\x82\xfd\xd5\xedw\ta\xdfD\x7f_\xb9\xb1T\xe0=\x1c3\xa3C\x17\xc5\xcc\xb8\x10q\x0f\xf3\xb4\xb7\x01L\x00L\x00\x0c\x0f\x81\xcc=$\xef\xa8\xaa\xfdX\xf9\xcb\x13\xfe\x92$\x80cU\xb7\x03}\xfa\x8f\x90\xf7\xe2-\x02\x00\xc9\xd4\x0f\x8f\xa0\x88\xc8\xa8r\x81cT\xc8\x90\t\x80Q)\xa2\xfe\x90\xbe\x8b\x0c>\x959\x82\xfd\xfd?\x14\x84\xdf\r\x1c\x9b\xdew\xb0\xd2\xb9[\xb5\xedD\x1b\xc5\xbd\xe8\xcc?\x1d\x02\x80`\xaf\xdb\xb4\x8b\xf2\xf7\x1c\xa3\xbc\xdd\xf7\x95\n\xbc\x87cp,\x13\x00#(\x08\x009\xfcH\xe3U\xb1\xf6\xc3\xc8\x87}\xbe*\x01\xe0X|F\xc5;\x80{H\xcf9\xe45\x02\xc0\xea\x0e\x01/:q\x9e\n\x8f\x9f-\x15x\x0f\xc7\xe0X&\x00FP\x10\x00\ny \x97\xdfj~\xc0\xcd\x07\x95\xfe;\r\r\xe0;s\x1b\x10#>\xab\x12\x14\x84{\xf1&\x01`\x95\x87\xa0\x1f:v\xa6T\xe0=\x1c\xc3\x04\xc0\xc2\xc1\x04\xe0\x10\x01\\f\x02`\x02`\x04\xf3\x16`\xa6\xdfl\x01\x98\x00\x98\x00\x18Aj\x04d\x02`\x02`x\xe8\x06\x84K\xef\xb2\x86\x1b\xf0\xb2\x1f\xb9\x01\x99\x00\x98\x00\x18\x8e\x04\x02uV\x0e\x04B\xd0\x90\xbf\x04\x021\x010\x010\x1c\x0c\x05\xbel\x19\n\xdc\xd9\xafB\x81\x99\x00\x98\x00\x18e%\x03\xed8&\xd3ruBa\xa1\xdac\x7f\x0f\xc3 \x04\xfe\xb2\x99\x0c\x84\xff\xf9c2\x10\x13\x00\x13\x00\xa3\x9cm\xc0\xac4\xfb\xe9\xc0p\xf3\xc5\xd8L\x07\x0e\x13\xd7\x9c\xe5\x83t`&\x00&\x00F9\x05A\xb2P\x10D\xac\xc4\xbeN\xaa\xe9*\xae\x99\xe5\x83\x82 L\x00\x15A\x00e\xf4\x8ec8\x8b\\GJl\x17\xd3\xed+}\\\x12L\\\xebv\x1f\x95\x04c\x02\xf0)\x01\xb8&&J=\xad\xcb> \xcf\xcb\xf0\x0e\xf0|]]wN:\xd2pc\xd2\xb4\x05T\xa3FM\xaf\x0b?\xb6\x1b\xb8\x96\xaf\x8a\x822\x01\xf8\x88\x00\xdcu\xe5\x93S\x96Pb\xa7\x9e\x14\x15\xddH\x9e\x9b\xe1\x1d\xe0\xf9\xe29\'\xcfZ"\x9f\xbbg\xbf\x9f\xbb,\xf8T\xaf\x97\x05\x1f\xe9\xe3\xb2\xe0L\x00>!\x00\x97\xf0\x0f\xbdq\x02U\xf7Aii\xc6\x8f\xc0\xf3\x1e\x964Q>\x7f\xbfn\x0c"V~\x08\xbf\xaf\x1b\x830\x01\xf8\x80\x00\xf0Y\xacD,\xfc\x15G\x02x\xfeN\x08\x16Vg\xa8\xe8\r\x1cn\r\x86s\xe6\xec\xf4}k0&\x00o\x13\x80\xb9\xe7\x87:\xca\xc2Xq\xc0\xf3\xb7[f\xbb\xb4\xe6\xa00\xd2\xc1;\x10\x16V\xcb\xa3U\x1f\xd6~\x9c\xab\xa2\x9a\x832\x01x\x99\x00\xf09\x18\xa4\xb0\'eA\xac8\xe0\xf9\xe3wp\xca\x9b\x03\x0b=\xdct\xb3\x17\xac\x91B\\/\\\xbd=8\xe6\x94\xbb=xV\x05\xb7\x07g\x02\xf0\x01\x01\xf8K\x9f\xb6`\x86\xd7\xdc\xb9\x05\xc52Z\x0f!\xbb\x88\xdbG\xf2\x0e2\xf8\x90\xc6\x8bz\x02@\xacx\x8d\xff\xe1\xbd\t\xe2\x18\x1c\x8b\xcf\xb8\x82|Nz!\x8c\x99\t\x80\t\x80\xe1\xd3\x80.\xac\xe2\x10hd\xee!\x95\x189\xfc(\xe4\x01\xe05\xfe\x87\xf7p\x8c\xd3+>\x13\x00\x13\x00\xc3\x8f":\xcb\x0cL\xf2a=\x03&\x00&\x00F\x90\x86t3\x01\x04(\x01\x84\x86\x86Rtt\x0c5j\x14\'\xd0\x88a\x898\xf9\xbc\xf0\xdc\x98\x00\x98\x00\x02\x9e\x000\x99\xcf\x9c}\x9a.\xbd\xfd.\xbdq\xe92\xc3\x02xNx^xnL\x00L\x00\x01O\x00X\xd10\xa9\xbf\xfa\xfa\x8ft\xe5w\x7f`X\x00\xcf\t\xcf\x0b\xcf\x8d\t\x80\t\xa0\x12\x10@#\xb9\xb2ar\xff\xf6\xca\xff0,\x80\xe7\x84\xe7\x85\xe7\xc6\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04\xc0\x04`?\xad;Pj\x192\x010\x010\x018\xf6;\xfa\xb6\x8e\xa3\x13\xb5\x0c\x99\x00\x98\x00\x98\x00\x1c\xf8\x1d+\xa2\x8e\xa3\x13\xb5\x0c\x99\x00\x98\x00\x98\x00<\xfe\x1d+\xb6\x8e\xa3\'\xb5\x0c\x99\x00\x98\x00\x98\x00<\xfc\x1d\xfd\xa1\x8e\xa3\xddZ\x86L\x00L\x00L\x00\x9e\xfc\x8e~T\xc7\xd1N-C&\x00&\x00&\x00\x0f~G\x7f\xaa\xe3h\xa7\x96!\x13\x00\x13\x00\x13\x80\x87\x04\xe0/E\\\xec\x1a/\x99\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x98\x00\x9c%\x80\xd0\x90*\xd4(\xaa\x0e\xc5G\xd7\xd3\x02>\x83\xcf2\x010\x010\x01\x040\x01@\x90/\x1dK\xa5\xdf\x9d_FW\xce-U\x02\x8e\xc5g\xf0Y&\x00&\x00&\x80\x00&\x00\xac\xe6\x10hzg\x03\xd1\xdb\xeb\xd5 \x8e\xc5g\xf0Y&\x00&\x00&\x80\x00\'\x00\xac\xeaR\xb0\xdf\xcaT\x838\x16\x9fa\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`\x02`0\x010\x010\x010\x98\x00\x98\x00\x98\x00\x18L\x00L\x00L\x00\x0c&\x00&\x00&\x00\x06\x13\x00\x13\x00\x13\x00\x13\x00\x87\x02{N\x00\xf9{\x8eQ\xd1\x89\xf3R\xd0K\x03\xde\xc31L\x00L\x00L\x00\x95,\x19\xa8~x\x04\xad\xdb\xb4K\n8V\xf9\xd2\x80\xf7p\x0c\x8ee\x02`\x02`\x02\xa8D\xe9\xc0!!!R\xb0\xb1\xba\x97\x07\x1c\x83c\x99\x00\x98\x00\x98\x00*QA\x10\xa7\xc1\x04\xe0\x11\x01\xc4\xd1\xa5\xb7\xdf\xa5\xaf\xbe\xfe\xa3\x9c\xdc\x8c\xf2\x81\xe7\x84\xe7\x85\xe7\xc6\x04\xc0\x04\x10\xf0\x04\x10\x1d\x1dCg\xce>-\'5V6F\xf9\xc0s\xc2\xf3\xc2sc\x02`\x02\x08x\x02\x08\r\r\x95\x93\x19+\x1a\xd4Z\x86\x15\xe2\xe4\xf3\xc2sc\x02\xf0\x1f\x02\xd8q\xe6k\xba\xe7\r&\x00\xbf\x9bL\xc1\x0cn\x0c\xe2\x1b\x84\xd5\xaeG\xb33\xee\xa5\xfd\xcf\xff\xdd\xe7$\xc0\x04\xc0\xa8|\xad\xc1:\x9b\xad\xc1\xee>\x190s\xaeF\xcd:\xd4kD2\xad9\xf4*\x15\xbe\xfa\x03\x1dy\x83\t\x80\t \xc0T\xe9\xbc=\xc5A\xd1\x1c\xd4\x9b\x08\x8f\x8a\xa31\xb3\xd2)\xef\xf4\x17R8\xbdm\x17`\x02`8\xfa;\xa257ZtWd{\xf0l/\xb7\x07\xf76\xaaT\xa9BM\xdat\xa3\x94\xb5\x87\xa9\xe0\xc2\x9f\xbd\xba-\xf0[\x02\xf0\x97\xfdd0\xc3\xee^\x1a$\x90<k\xa9\xdc\x0e\xe0\x1c\x98\x0f\xde\x04\xae\x81k\xe1\x9a\xb8\xb6\x9dy\xa7I\x00?\x08|-pE\x01\x7f\xb3\xfb\xfc\xabU\x0f\xa3.\x03\xc7\xd1\xca\xbd\xcf\xd1\xa1\x97\xff\xe5\x95m\x81_\x12\x80?\xed\'\x83\x19v\xf6\xd2%\xb7\x03\xf8,\x08\x04s\xc1\x9b\xc05p-\\\xd3\xd6|\xd3\'\x00\x08\x7f/\x818\x81\xf8r\x80\xf73\x05\xfe\xe3\xc9\xefP\'<\x8a\x86O]J9\xc5\x9f8\xbe-\xf0O\x02\xf0\x93\xfdd0\xc3\xee^\xfaz"\xcf\xf3\x11r=\xb9O}\x02\xb8b\n\xb7\xca\x88\x168\xed\xc4o\x12\xd7"\x91\xa6-/\xa0\xdd\xe7\xff\xe0\xda\x16\xbc^\x89\t\xa0\xa2\xf7\x93\xc1.\xfcv\xf7\xd2\x81\n\x1b\x04\x10o\xa8\x0f\x1c\xbbG\xe0\x8f\x9e\xfe6\xa1U\xabQb\xef\x91\xb4t\xc7Y:\xf8\xe2\xf7\x1e\xdb\x07\xfc\x9a\x00*b?\x19\xccpb/\xcd\x04P\xe6\xa8.0B\xe0\xac\xc0\xf7\x9e\x12A\xad\xba\x114p\xdc<Z\x7f\xf4\x9d\xab\x82\\\xe9\x08\xa0"\xf6\x93\xc1\x0c\'\xf6\xd2L\x00\x96#B M\xe0\xb2#\x86\xda\xb8\x04\x9a\xb8(\x8f\xb6?\xf1;i$\xd4%\x82\x80 \x00_\xef\'\x83\x19\xb9A\xb4\xeaW\x10\x01\xb8GK\x81<\xd3\xa0\xe8\x11\t\x84\x84\x84R\xab\xce\xfd)-\xbb\x98\xf6=\xf77\xadmA\xe0\x10\x00\x83Q\xb9\x08\x00#T`\x80\xc0)O\xdc\x85%\xa3\t{\x8f\x9cFk\x0b/*G\x132\x010\x18\x15G\x00\xeeQG`\xba\xc0\x1b\x9e\xba\x0ce4aCW4a\xfe\xe9_[n\x0b\x98\x00\x18\x8c\x8a\'\x00\xf7hb\xc6\r\xfc\xc6\x89h\xc2\xa6m\xbb\xd3\xacuG\xa8\xe0\xc27en\x0b$\x01<\xce\x04\xc0`\x02\xf0\x07\x02\xc0\xa8"\xd0S\xe0\x98\xc0_<%\x02D\x13v\x1b4\x9eV\xed{\x81\n_\xf9\xf7O\xb6\x05 \x86\x9c\x93\x1fS\xbd\xc8\x18\x95\xf3}\xcf\x04\xc0`\x02\xf0.\x01\xb8GM\x81\x89\x02/\n\xfc\xdbS"\xa8\x17\x11M#\x93W\xd0\xe6\xe2O]\xd1\x84o\xb8\x84\x1f\xaf\xa7.\xdd)\xe3\x0b\x14\xce\xf3{\xdc\xd8?\xad\x0e\xac[/\x9cVd\xecb\x02`\x04\x14\x01\xac\xc8\xd8)\xe7\xae\x82 |\xa1\x11\t\xe8\xe9\x88\x11X%\xf0\x99#\xd1\x84\t\x1d(y\xf9\x1e\xda|\xeaS\xdar\xea3J\xbe\xf3n\xaa\x1f\xa5\x9css\x117\xf4\'\xcb\x02\x07a\xb5h\xee\xe2\x0c\xca/(\xe6\xc9\xc5\x08\x08`\xae\xce]\x9c.\xe7\xae\x82 \xbcg\x86\xf8\xfart\x148\xe0T4a\xfd\x06\xb1\x02\x8d\xc4\xeb\xea:\x9f\xddg\x98_\xde\xf2\xe0\xe1\xa3&\xb1\x06\xc0\x08(\r\x00sVQ\x10.\x08\xd43|?\x10Mx\xa3\xc0\x93*\x9a\xb8\xc3\xf8_\x81\x9bq\x13\x0f\xa9| &6^\xaaTy\xac\x050\x02`\xf5\xc7\\\x8d\x8eU\xb6\x84\x1f4}\xf8\x155"\x05\x16\xa9.\xc6\x0e\xe1I\xf3\xba\xc6J\x81\x7f\xa9|\xa8[\xaf\x81\xb4>\xf70\x93\x00\xc3\xaf\x85\x1fs\x14sUQ\x10~0Cy\xfda \x9ap\x9bi\x9c\xf3\xa6\xf0\x7f+0\xc5}\xd1\x1e\x02_\xaa\x86(\xe2\xc1\xaeH\xdf)U,<\xec\xa0\x0b\xadur\xc2^s\xde\x93\x8e\xab\xc0\xc1\x04\xf7\\\xc4\xdc\xc4\x1c\xc5\\U\x14\x06x\x00:\x19\xfe3\xaa\n\x0c2S\x8e\xff\xe1%\x02(4\xbd\x12W\xdd\x13\xf7\xeb\x9c\x00\xdb\x01\xec\xaf`d\x81\xaa\x15\x0c\x895k\xb3\xf6Q\xe6\x96"\xda\xb2\xfb\x01G\x88\xa0dB\x14\x90\xe5P\xd2\x0e\xeem\xcb\xee\xfb\xe5\xbd\xe2\x9e\x83\xe1\xb7\xc1\x1c\xc4\\\xc4\x9c\xd4P\xfb\xddx@ \xcc\xf0\xbfQW E\xe0\x92\xc0\x7f\x1d\x14~\xd8;\x9a]\x7f\xb1\x9b\xec\x04)\xc0\xc2\n7K0\xa4\xd6\x86GDQ|\xd3\x964h\xf8\xcd\xb4<}\x87G\xe5\xd1\\)\xd1K\xae\xa6D\x03\x1d:\xf7\xf28m\x17\x9f[\xben\x87\xbcG\xdc+\xee9\x18~\x1b\xccAEk\xff\xf5\xc0\x9c\x1fc\xf8\xf7h*\xb0I\xe0\xb7\x0e\x08\xff\xd3\x02\x89\xa5]\xa4\x96\xc9\x84\\@C\x01\xf1M\x13h\xf1\x8a\xcd\xb6\x04\xb5\xbc\xa2(\xee\xc2\x1dY6\x8b`.^\x91C\x8d\xc5\xbd\xf1o\xa4\xb5\xfa\xd72\xfc\x7f\x84\x98%\xcb\xecF\x13\xfe\xd54t6-\xef"\x08W\xfc\x9c\'\x85\x1a\xda\xb4\xefB\xebs\x8b4\x0blZ\x97Es\x95\xeeZ\xaa\xb5\x1d\xc0=\xe0^pO\xfc\xdb(\xe3ss\xce\x07\xd2\x00Y\xdd"\xf0\x98\xc0\x9f\x155\x1c\xac\xfa\x93K\xee\xf9\xcb\x1b\xa9&[\xf0\x04Q(\xb35+m\xb5zp\x94FaTl\x07\xb24\x8aw\xe2\x1eR\xe6\xaf\xe6Rkz\xaa\xff\x1c#p\x07\xec\x03\xc3\x05\xb6\x08\x9c\x13\xf8H\xe0+\x13\x9f\x98.\xbe|\x81$\x81p\xdd\xc0\x84L/Z\x1f+\x15F\x8e\x99\xfa\x97\xad{O]\x11Bh\t\xb1J_Y\x9b\xb5\xff\xeb\x06Q1?X\x9d\x17\xc7\xe0X|F\xe5\xdc\xb8\x07\xdc\x0b\xff&J\xf8N \xc3\x9c\xeb\x95a\xd45\xc3\x8b\x9b\x99\x885\xff\xe7Q\xd2B:k\x02\n\t\x19\xe1\x91\xd9G\x1f\xbe\x18+\x840\xde\n\xbb\x0b\x1f\x8f\x1b1zr\xb7\x90\x90\x90_Z\xbb[C~\x89cw\x15>\x16\xa7r\xee\xa3\x8f\\\x8c\x15\xf7\x92\xc3\xbf\x89\xd2\xca\x9f\x19 \xfb\xfe\n\x1d\xd5\xcd\xed\x00\xdb\x04\xca\x0f\xa6\x18\xd3\xad\xd7@C\x08\xa1%f\xa4.w\x93\xeb\xa3\n\xe7\x86\x0f\xb8\xe6m\xa9+\x94\xce\x8d{0=9\xdf\xf2\xefR\xee\x9e\x7fN%Z\xf9}2z\x9a\x96\xd2ox\x02\xfd\x04\xd8{E\xd8x\xa6S-\x04\xf5[\xf3\x18;\xe1\xa4\xe7\xf9w)u\xd5\x7f \x00\r~~ey\x1ce>\xc4+f\xe8d\xb0O\xaaK\xa6[\xc6\xee\x16+\xab\x0c\x12\xf8\xd6|\xcfn`J/\xf3\xde\x82\xfd\xf7\xf9\xb79W1g\xc7\xb2\xca\xef\xcc\xc0\xa4D\xc8d\x9a\xe9SDD\x11\x92\x17\xbe0\xd4z\xaa\x05:~#\xf0\xa6i]m\xeb\xe1\xb3\xaci\xae\xf2\x8f\x9aV\xdbO\xcc\xd7SU\xdd5\xe5\x8c\xb6\xe6=\xbei\xdes0\xfc6_\x98s\xf1\x8297\xd3\xcc\xb9\x1a\xc6b\xeb\x9d\x81\xcc)\xa4O"\x87\xda\xaa\x9fZeAc\x81\x06fP\x86\x93\xdaU\xac\t\'W\xa9\x10\xf3^\x1b\x07\xc9o\x13g\xce\xc5zF\xc5f\xf5\xf1\xe0\xc1\x83\x07\x0f\x1e<x\xf0\xe0\xc1\x83\x07\x0f\x1e<x\xf0\xe0\xc1\x83\x07\x0f\x1e<x\xf8\xc9\xf8?\x1d?\x04l\xc9\x9as\xe4\x00\x00\x00\x00IEND\xaeB`\x82'

    # Ścieżka do pliku tymczasowego
    katalog_tymczasowy = tempfile.gettempdir()
    sciezka_ikony  = os.path.join(katalog_tymczasowy, "temp_app_icon.ico")

    # Sprawdza, czy plik już istnieje i jest aktualny
    if not os.path.exists(sciezka_ikony ) or os.path.getsize(sciezka_ikony ) != len(ikona_w_bajtach):
        try:
            with open(sciezka_ikony , "wb") as plik_ikony:
                plik_ikony.write(ikona_w_bajtach)
        except Exception as e:
            print(f"\nBłąd zapisu ikony: {e}")
            return None

    return sciezka_ikony


root = tk.Tk()
root.title("System do zarządzania siecią kin")
root.geometry("1200x800")

myappid = u'System.do.zarzadzania.siecia.kin'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
sciezka_ikony  = pobierz_sciezke_ikony()
if sciezka_ikony :
    root.iconbitmap(sciezka_ikony)
else:
    print("\nNie udało się załadować ikony")

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="lightblue")
style.configure("TLabel", background="lightblue", foreground="black")
style.configure("TButton", background="skyblue", foreground="black")
style.configure("TNotebook", background="skyblue")
style.configure("TNotebook.Tab", background="lightblue", foreground="black", padding=[5, 2])
style.map("TNotebook.Tab", background=[("selected", "skyblue"), ("active", "skyblue")])
# style.configure("TEntry", fieldbackground="lightblue", foreground="black")
style.configure("TLabelframe", background="lightblue")
style.configure("TLabelframe.Label", background="lightblue", foreground="black")
style.configure("Map.TButton", background="skyblue", foreground="black", padding=5)
style.configure("Group.TLabelframe", background="lightblue", padding=0)
style.configure("Group.TLabelframe.Label", background="lightblue", anchor="center", padding=0)

zakladki = ttk.Notebook(root)
zakladki.pack(fill="both", expand=True)
zakladki.bind("<<NotebookTabChanged>>", aktualizuj_po_zmianie_zakladki)

# --- Zakładka kina --- #

zakladka_kin = ttk.Frame(zakladki)
zakladki.add(zakladka_kin, text="Kina")

ramka_filtru_kin = ttk.Frame(zakladka_kin)
ramka_filtru_kin.grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.Label(ramka_filtru_kin, text="Wybierz sieć kin:").pack(side="left")
lista_rozwijalna_filtru_kin = ttk.Combobox(ramka_filtru_kin, state="readonly", width=20)
lista_rozwijalna_filtru_kin.pack(side="left", padx=5)
lista_rozwijalna_filtru_kin['values'] = ["Wszystkie"]
lista_rozwijalna_filtru_kin.set("Wszystkie")
lista_rozwijalna_filtru_kin.bind("<<ComboboxSelected>>", lambda e: odswiez_liste_kin())

ramka_listy_kin = ttk.Frame(zakladka_kin)
ramka_listy_kin.grid(row=1, column=0, padx=10, pady=2, sticky="ns")
ttk.Label(ramka_listy_kin, text="Lista kin:").pack()
lista_kin = tk.Listbox(ramka_listy_kin, width=60, height=25)  # , bg="lightblue", fg="black" - jako kolor tabeli
lista_kin.pack()
lista_kin.bind("<<ListboxSelect>>", pokaz_szczegoly_kina)

ramka_przyciskow_kin = ttk.Frame(ramka_listy_kin)
ramka_przyciskow_kin.pack(pady=5)

przycisk_edytuj_kino = ttk.Button(ramka_przyciskow_kin, text="Edytuj", command=edytuj_kino)
przycisk_edytuj_kino.grid(row=0, column=0, padx=5)

przycisk_usun_kino = ttk.Button(ramka_przyciskow_kin, text="Usuń", command=usun_kino)
przycisk_usun_kino.grid(row=0, column=1, padx=5)

etykieta_szczegoly_kina = ttk.Label(ramka_listy_kin, text="Szczegóły kina:")
etykieta_szczegoly_kina.pack(pady=10)

informacje_o_wybranym_kinie = ttk.Label(ramka_listy_kin, text="Nie wybrano kina.", anchor="w", justify="left")
informacje_o_wybranym_kinie.pack(pady=5, fill="both", expand=True)

ramka_formularza_kin = ttk.Frame(zakladka_kin)
ramka_formularza_kin.grid(row=1, column=1, padx=10, pady=5, sticky="n")
ttk.Label(ramka_formularza_kin, text="Dodaj/Edytuj kino:").grid(row=0, column=1, columnspan=2, pady=5)

ttk.Label(ramka_formularza_kin, text="Sieć kina:").grid(row=1, column=0, sticky="e")
pole_kino_siec = ttk.Entry(ramka_formularza_kin, width=33)
pole_kino_siec.grid(row=1, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_kin, text="Nazwa kina:").grid(row=2, column=0, sticky="e")
pole_kino_nazwa = ttk.Entry(ramka_formularza_kin, width=33)
pole_kino_nazwa.grid(row=2, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_kin, text="Lokalizacja:").grid(row=3, column=0, sticky="e")
pole_kino_lokalizacja = ttk.Entry(ramka_formularza_kin, width=33)
pole_kino_lokalizacja.grid(row=3, column=1, padx=2, pady=5)

przycisk_dodaj_kina = ttk.Button(ramka_formularza_kin, text="Dodaj", command=dodaj_kino)
przycisk_dodaj_kina.grid(row=4, column=1, columnspan=2, pady=10)

# --- Zakładka seanse --- #

zakladka_seanse = ttk.Frame(zakladki)
zakladki.add(zakladka_seanse, text="Seanse")

ramka_seans_filtr = ttk.Frame(zakladka_seanse)
ramka_seans_filtr.grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.Label(ramka_seans_filtr, text="Wybierz kino:").grid(row=0, column=0, sticky="w")
lista_rozwijalna_seans_kino = ttk.Combobox(ramka_seans_filtr, state="readonly", width=20)
lista_rozwijalna_seans_kino.grid(row=0, column=1, padx=5)
lista_rozwijalna_seans_kino['values'] = ["Wszystkie"]
lista_rozwijalna_seans_kino.set("Wszystkie")
lista_rozwijalna_seans_kino.bind("<<ComboboxSelected>>", lambda e: odswiez_liste_seansow())

ramka_listy_seans = ttk.Frame(zakladka_seanse)
ramka_listy_seans.grid(row=1, column=0, padx=10, pady=2, sticky="ns")
ttk.Label(ramka_listy_seans, text="Lista seansów:").pack()
lista_seansow = tk.Listbox(ramka_listy_seans, width=59, height=25)  # , bg="lightblue", fg="black" - jako kolor tabeli
lista_seansow.pack()
lista_seansow.bind("<<ListboxSelect>>", pokaz_szczegoly_seansu)

ramka_przyciskow_seans = ttk.Frame(ramka_listy_seans)
ramka_przyciskow_seans.pack(pady=5)

przycisk_edytuj_seans = ttk.Button(ramka_przyciskow_seans, text="Edytuj", command=edytuj_seans)
przycisk_edytuj_seans.grid(row=0, column=0, padx=5)

przycisk_usun_seans = ttk.Button(ramka_przyciskow_seans, text="Usuń", command=usun_seans)
przycisk_usun_seans.grid(row=0, column=1, padx=5)

etykieta_szczegoly_seansu = ttk.Label(ramka_listy_seans, text="Szczegóły seansu:")
etykieta_szczegoly_seansu.pack(pady=10)

informacje_o_wybranym_seansie = ttk.Label(ramka_listy_seans, text="Nie wybrano seansu.", anchor="w", justify="left")
informacje_o_wybranym_seansie.pack(pady=5, fill="both", expand=True)

ramka_formularza_seans = ttk.Frame(zakladka_seanse)
ramka_formularza_seans.grid(row=1, column=1, padx=10, pady=5, sticky="n")
ttk.Label(ramka_formularza_seans, text="Dodaj/Edytuj seans:").grid(row=0, column=1, columnspan=2, pady=5)

ttk.Label(ramka_formularza_seans, text="Tytuł:").grid(row=1, column=0, sticky="e")
pole_seans_tytul = ttk.Entry(ramka_formularza_seans, width=33)
pole_seans_tytul.grid(row=1, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_seans, text="Data:").grid(row=2, column=0, sticky="e")
pole_seans_data = ttk.Entry(ramka_formularza_seans, width=33)
pole_seans_data.grid(row=2, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_seans, text="Godzina:").grid(row=3, column=0, sticky="e")
pole_seans_godzina = ttk.Entry(ramka_formularza_seans, width=33)
pole_seans_godzina.grid(row=3, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_seans, text="Czas trwania:").grid(row=4, column=0, sticky="e")
pole_seans_czas_trwania = ttk.Entry(ramka_formularza_seans, width=33)
pole_seans_czas_trwania.grid(row=4, column=1, padx=2, pady=5)

przycisk_dodaj_seans = ttk.Button(ramka_formularza_seans, text="Dodaj", command=dodaj_seans)
przycisk_dodaj_seans.grid(row=5, column=1, columnspan=2, pady=10)

# --- Zakładka pracownicy --- #

zakladka_pracownicy = ttk.Frame(zakladki)
zakladki.add(zakladka_pracownicy, text="Pracownicy")

ramka_pracownik_filtr = ttk.Frame(zakladka_pracownicy)
ramka_pracownik_filtr.grid(row=0, column=0, padx=10, pady=5, sticky="w")

ttk.Label(ramka_pracownik_filtr, text="Wybierz kino:").grid(row=0, column=0, sticky="w")
lista_rozwijalna_pracownik_kino = ttk.Combobox(ramka_pracownik_filtr, state="readonly", width=20)
lista_rozwijalna_pracownik_kino.grid(row=0, column=1, padx=5)
lista_rozwijalna_pracownik_kino['values'] = ["Wszystkie"]
lista_rozwijalna_pracownik_kino.set("Wszystkie")
lista_rozwijalna_pracownik_kino.bind("<<ComboboxSelected>>", lambda e: odswiez_liste_pracownikow())

ramka_listy_pracownik = ttk.Frame(zakladka_pracownicy)
ramka_listy_pracownik.grid(row=1, column=0, padx=10, pady=2, sticky="ns")
ttk.Label(ramka_listy_pracownik, text="Lista pracowników:").pack()
lista_pracownikow = tk.Listbox(ramka_listy_pracownik, width=60,height=25)  # , bg="lightblue", fg="black" - jako kolor tabeli
lista_pracownikow.pack()
lista_pracownikow.bind("<<ListboxSelect>>", pokaz_szczegoly_pracownika)

ramka_przyciskow_pracownik = ttk.Frame(ramka_listy_pracownik)
ramka_przyciskow_pracownik.pack(pady=5)

przycisk_edytuj_pracownik = ttk.Button(ramka_przyciskow_pracownik, text="Edytuj", command=edytuj_pracownika)
przycisk_edytuj_pracownik.grid(row=0, column=0, padx=5)

przycisk_usun_pracownik = ttk.Button(ramka_przyciskow_pracownik, text="Usuń", command=usun_pracownika)
przycisk_usun_pracownik.grid(row=0, column=1, padx=5)

etykieta_szczegoly_pracownika = ttk.Label(ramka_listy_pracownik, text="Szczegóły pracownika:")
etykieta_szczegoly_pracownika.pack(pady=10)

informacje_o_wybranym_pracowniku = ttk.Label(ramka_listy_pracownik, text="Nie wybrano pracownika.", anchor="w",justify="left")
informacje_o_wybranym_pracowniku.pack(pady=5, fill="both", expand=True)

ramka_formularza_pracownik = ttk.Frame(zakladka_pracownicy)
ramka_formularza_pracownik.grid(row=1, column=1, padx=10, pady=5, sticky="n")
ttk.Label(ramka_formularza_pracownik, text="Dodaj/Edytuj pracownika:").grid(row=0, column=1, columnspan=2, pady=5)

ttk.Label(ramka_formularza_pracownik, text="Imię:").grid(row=1, column=0, sticky="e")
pole_pracownik_imie = ttk.Entry(ramka_formularza_pracownik, width=33)
pole_pracownik_imie.grid(row=1, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_pracownik, text="Nazwisko:").grid(row=2, column=0, sticky="e")
pole_pracownik_nazwisko = ttk.Entry(ramka_formularza_pracownik, width=33)
pole_pracownik_nazwisko.grid(row=2, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_pracownik, text="Lokalizacja:").grid(row=3, column=0, sticky="e")
pole_pracownik_lokalizacja = ttk.Entry(ramka_formularza_pracownik, width=33)
pole_pracownik_lokalizacja.grid(row=3, column=1, padx=2, pady=5)

przycisk_dodaj_pracownik = ttk.Button(ramka_formularza_pracownik, text="Dodaj", command=dodaj_pracownika)
przycisk_dodaj_pracownik.grid(row=4, column=1, columnspan=2, pady=10)

# --- Zakładka klienci --- #

zakladka_klienci = ttk.Frame(zakladki)
zakladki.add(zakladka_klienci, text="Klienci")

ramka_klient_filtr = ttk.Frame(zakladka_klienci)
ramka_klient_filtr.grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.Label(ramka_klient_filtr, text="Wybierz kino:").grid(row=0, column=0, sticky="w")
lista_rozwijalna_klient_kino = ttk.Combobox(ramka_klient_filtr, state="readonly", width=20)
lista_rozwijalna_klient_kino.grid(row=0, column=1, padx=5)
lista_rozwijalna_klient_kino['values'] = ["Wszystkie"]
lista_rozwijalna_klient_kino.set("Wszystkie")
lista_rozwijalna_klient_kino.bind("<<ComboboxSelected>>", lambda e: odswiez_liste_klientow())

ramka_listy_klient = ttk.Frame(zakladka_klienci)
ramka_listy_klient.grid(row=1, column=0, padx=10, pady=2, sticky="ns")
ttk.Label(ramka_listy_klient, text="Lista klientów:").pack()
lista_klientow = tk.Listbox(ramka_listy_klient, width=60, height=25)  # , bg="lightblue", fg="black" - jako kolor tabeli
lista_klientow.pack()
lista_klientow.bind("<<ListboxSelect>>", pokaz_szczegoly_klienta)

ramka_przyciskow_klient = ttk.Frame(ramka_listy_klient)
ramka_przyciskow_klient.pack(pady=5)

przycisk_edytuj_klient = ttk.Button(ramka_przyciskow_klient, text="Edytuj", command=edytuj_klienta)
przycisk_edytuj_klient.grid(row=0, column=0, padx=5)

przycisk_usun_klient = ttk.Button(ramka_przyciskow_klient, text="Usuń", command=usun_klienta)
przycisk_usun_klient.grid(row=0, column=1, padx=5)

etykieta_szczegoly_klienta = ttk.Label(ramka_listy_klient, text="Szczegóły klienta:")
etykieta_szczegoly_klienta.pack(pady=10)

informacje_o_wybranym_kliencie = ttk.Label(ramka_listy_klient, text="Nie wybrano klienta.", anchor="w", justify="left")
informacje_o_wybranym_kliencie.pack(pady=5, fill="both", expand=True)

ramka_formularza_klient = ttk.Frame(zakladka_klienci)
ramka_formularza_klient.grid(row=1, column=1, padx=10, pady=5, sticky="n")
ttk.Label(ramka_formularza_klient, text="Dodaj/Edytuj kienta:").grid(row=0, column=1, columnspan=2, pady=5)

ttk.Label(ramka_formularza_klient, text="Imię:").grid(row=1, column=0, sticky="e")
pole_klient_imie = ttk.Entry(ramka_formularza_klient, width=33)
pole_klient_imie.grid(row=1, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_klient, text="Nazwisko:").grid(row=2, column=0, sticky="e")
pole_klient_nazwisko = ttk.Entry(ramka_formularza_klient, width=33)
pole_klient_nazwisko.grid(row=2, column=1, padx=2, pady=5)

ttk.Label(ramka_formularza_klient, text="Lokalizacja:").grid(row=3, column=0, sticky="e")
pole_klient_lokalizacja = ttk.Entry(ramka_formularza_klient, width=33)
pole_klient_lokalizacja.grid(row=3, column=1, padx=2, pady=5)

przycisk_dodaj_klient = ttk.Button(ramka_formularza_klient, text="Dodaj", command=dodaj_klienta)
przycisk_dodaj_klient.grid(row=4, column=1, columnspan=2, pady=10)

# --- Zakładka mapy --- #

zakladka_mapy = ttk.Frame(zakladki)
zakladki.add(zakladka_mapy, text="Mapa")

widget_mapy = tkintermapview.TkinterMapView(zakladka_mapy, width=1100, height=630, corner_radius=0)
widget_mapy.pack(pady=10)
widget_mapy.set_position(52.23, 21.00)
widget_mapy.set_zoom(6)
root.after(100, odswiez_mape)

ramka_list_rozwijalnych = ttk.Frame(zakladka_mapy)
ramka_list_rozwijalnych.pack(pady=5)

etykieta_siec = ttk.Label(ramka_list_rozwijalnych, text="Wybierz sieć kin:")
etykieta_siec.grid(row=0, column=0, padx=5, pady=2, sticky="e")
lista_rozwijalna_siec_mapy = ttk.Combobox(ramka_list_rozwijalnych, state="readonly", width=20)
lista_rozwijalna_siec_mapy.grid(row=0, column=1, padx=5, pady=2, sticky="w")

etykieta_kino = ttk.Label(ramka_list_rozwijalnych, text="Wybierz kino:")
etykieta_kino.grid(row=0, column=2, padx=5, pady=2, sticky="e")
lista_rozwijalna_kino_mapy = ttk.Combobox(ramka_list_rozwijalnych, state="readonly", width=20)
lista_rozwijalna_kino_mapy.grid(row=0, column=3, padx=5, pady=2, sticky="w")

etykieta_seans = ttk.Label(ramka_list_rozwijalnych, text="Wybierz seans:")
etykieta_seans.grid(row=0, column=4, padx=5, pady=2, sticky="e")
lista_rozwijalna_seans_mapy = ttk.Combobox(ramka_list_rozwijalnych, state="readonly", width=20)
lista_rozwijalna_seans_mapy.grid(row=0, column=5, padx=5, pady=2, sticky="w")

ramka_list_rozwijalnych.columnconfigure(0, weight=1)
ramka_list_rozwijalnych.columnconfigure(6, weight=1)

odswiez_liste_sieci_na_mapie()
aktualizuj_kino_na_mapie_po_sieci()
aktualizuj_liste_seansow_na_mapie()

ramka_przyciski_mapy = ttk.Frame(zakladka_mapy)
ramka_przyciski_mapy.pack(pady=5)

# Ramki grupujące
ramka_kina = ttk.LabelFrame(ramka_przyciski_mapy, style="Group.TLabelframe")
ramka_kina.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
etykieta_kina = ttk.Label( ramka_przyciski_mapy, text="Operacje na kinach")
etykieta_kina.place(in_=ramka_kina, relx=0.5, y=-7, anchor="s")

ramka_seanse = ttk.LabelFrame(ramka_przyciski_mapy, style="Group.TLabelframe")
ramka_seanse.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
etykieta_seanse = ttk.Label( ramka_przyciski_mapy, text="Operacje na kinach")
etykieta_seanse.place(in_=ramka_seanse, relx=0.5, y=-7, anchor="s")

ramka_osoby = ttk.LabelFrame(ramka_przyciski_mapy, style="Group.TLabelframe")
ramka_osoby.grid(row=0, column=4, columnspan=2, padx=5, pady=5, sticky="nsew")
etykieta_osoby = ttk.Label( ramka_przyciski_mapy, text="Operacje na kinach")
etykieta_osoby.place(in_=ramka_osoby, relx=0.46, y=-7, anchor="s")

# Przyciski dla grup
przycisk_pokaz_kina = ttk.Button(ramka_kina, text="Pokaż wszystkie kina", command=pokaz_wszystkie_kina_na_mapie, style="Map.TButton")
przycisk_pokaz_kina.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_kina, "Wyświetla wszystkie kina na mapie")

przycisk_pokaz_placowki = ttk.Button(ramka_kina, text="Pokaż placówki sieci", command=pokaz_kin_po_sieci, style="Map.TButton")
przycisk_pokaz_placowki.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_placowki, "Wyświetla kina wybranej sieci na mapie")

przycisk_pokaz_szczegoly = ttk.Button(ramka_kina, text="Pokaż szczegóły", command=pokaz_szczegoly_kina_na_mapie, style="Map.TButton")
przycisk_pokaz_szczegoly.grid(row=0, column=2, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_szczegoly, "Pokazuje szczegóły wybranego kina na mapie")

przycisk_pokaz_kina_dla_seansu = ttk.Button(ramka_seanse, text="Pokaż kina dla seansu", command=pokaz_kina_dla_seansu, style="Map.TButton")
przycisk_pokaz_kina_dla_seansu.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_kina_dla_seansu, "Pokazuje kina dla wybranego seansu na mapie")

przycisk_pokaz_pracownikow = ttk.Button(ramka_osoby, text="Pokaż pracowników", command=pokaz_pracownikow_na_mapie, style="Map.TButton")
przycisk_pokaz_pracownikow.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_pracownikow, "Wyświetla pracowników wybranego kina/kin na mapie")

przycisk_pokaz_klientow = ttk.Button(ramka_osoby, text="Pokaż klientów", command=pokaz_klientow_na_mapie, style="Map.TButton")
przycisk_pokaz_klientow.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
podpowiedzi_przyciskow_na_mapie(przycisk_pokaz_klientow, "Wyświetla klientów wybranego kina/kin na mapie")
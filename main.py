import tkinter as tk
from tkinter import ttk

from gui_utils import *

root = tk.Tk()
root.title("System do zarządzania siecią kin")
root.geometry("1200x800")

zakladki = ttk.Notebook(root)
zakladki.pack(fill="both", expand=True)

# --- Zakładka Kin --- #

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
lista_kin.bind("<<ListboxSelect>>", lambda e: pokaz_szczegoly_kina)

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

# --- Zakładka Seanse --- #

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
lista_seansow.bind("<<ListboxSelect>>", lambda e: pokaz_szczegoly_seansu)

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

# --- Zakładka Pracownicy --- #

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
lista_pracownikow.bind("<<ListboxSelect>>", lambda e: pokaz_szczegoly_pracownika)

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

# --- Zakładka Klienci --- #

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
lista_klientow.bind("<<ListboxSelect>>", lambda e: pokaz_szczegoly_klienta)

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



root.mainloop()
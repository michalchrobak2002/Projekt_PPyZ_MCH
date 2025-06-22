import tkinter as tk
from tkinter import ttk
import tkintermapview

from gui_utils import *

root = tk.Tk()
root.title("System do zarządzania siecią kin")
root.geometry("1200x800")

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="lightblue")
style.configure("TLabel", background="lightblue", foreground="black")
style.configure("TButton", background="skyblue", foreground="black")
style.configure("TNotebook", background="skyblue")
style.configure("TNotebook.Tab", background="lightblue", foreground="black", padding=[5, 2])
style.map("TNotebook.Tab", background=[("selected", "skyblue")])
# style.configure("TEntry", fieldbackground="lightblue", foreground="black")
style.configure("TLabelframe", background="lightblue")
style.configure("TLabelframe.Label", background="lightblue", foreground="black")
style.configure("Map.TButton", background="skyblue", foreground="black", padding=5)
style.configure("Group.TLabelframe", background="lightblue", padding=0)
style.configure("Group.TLabelframe.Label", background="lightblue", anchor="center", padding=0)


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

# --- Zakładka Mapy --- #

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



root.mainloop()
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


root.mainloop()
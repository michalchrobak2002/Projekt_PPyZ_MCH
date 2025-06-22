import tkinter as tk

# --- Zakładka Kin --- #

def odswiez_liste_kin():
    pass

def pokaz_szczegoly_kina():
    pass

def edytuj_kino():
    pass

def usun_kino():
    pass

def dodaj_kino():
    pass

# --- Zakładka Seanse --- #

def odswiez_liste_seansow():
    pass

def pokaz_szczegoly_seansu():
    pass

def edytuj_seans():
    pass

def usun_seans():
    pass

def dodaj_seans():
    pass

# --- Zakładka Pracownicy --- #

def odswiez_liste_pracownikow():
    pass

def pokaz_szczegoly_pracownika():
    pass

def edytuj_pracownika():
    pass

def usun_pracownika():
    pass

def dodaj_pracownika():
    pass

# --- Zakładka Klienci --- #

def odswiez_liste_klientow():
    pass

def pokaz_szczegoly_klienta():
    pass

def edytuj_klienta():
    pass

def usun_klienta():
    pass

def dodaj_klienta():
    pass

# --- Zakładka Mapy --- #

def odswiez_mape():
    pass

def pokaz_wszystkie_kina_na_mapie():
    pass

def pokaz_kin_po_sieci():
    pass

def pokaz_szczegoly_kina_na_mapie():
    pass

def pokaz_kina_dla_seansu():
    pass

def pokaz_pracownikow_na_mapie():
    pass

def pokaz_klientow_na_mapie():
    pass

def podpowiedzi_przyciskow_na_mapie(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
    label.pack()

    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    tooltip.withdraw()
    return tooltip


########################################
def odswiez_liste_sieci_na_mapie():
    pass

def aktualizuj_kino_na_mapie_po_sieci():
    pass

def aktualizuj_liste_seansow_na_mapie():
    pass
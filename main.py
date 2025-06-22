import atexit
import os
import sys
import time
import threading
import requests

from utils import gui, controller, model

def sprawdz_polaczenie_internetowe():
    """ Sprawdza połączenie internetowe i aktualizuje globalny stan """
    try:
        requests.get("https://www.google.com", timeout=5)
        nowy_status = True
    except:
        nowy_status = False

    model.poprzedni_stan_internetu = model.czy_jest_internet
    if nowy_status != model.czy_jest_internet:
        model.czy_jest_internet = nowy_status

        if model.czy_jest_internet and not model.poprzedni_stan_internetu:
            gui.podlaczono_internet()
        elif not model.czy_jest_internet:
            gui.wyswietl_brak_internetu()

def uruchom_monitorowanie_internetu():
    """ Uruchamia w tle monitorowanie połączenia internetowego """
    def monitor():
        while True:
            sprawdz_polaczenie_internetowe()
            time.sleep(5)

    threading.Thread(target=monitor, daemon=True).start()

@atexit.register
def cleanup():
    try:
        os.remove(gui.pobierz_sciezke_ikony())
    except:
        pass


def zamykanie():
    """ Funkcja wywoływana przy zamykaniu aplikacji. Zapisuje dane i zamyka okno. """
    controller.zapisz_dane()
    gui.root.destroy()



uruchom_monitorowanie_internetu()
if getattr(sys, 'frozen', False):
    katalog_bazowy = os.path.dirname(sys.executable)
else:
    katalog_bazowy = os.path.dirname(os.path.abspath(__file__))

controller.ustaw_folder_danych(katalog_bazowy)

gui.root.protocol("WM_DELETE_WINDOW", zamykanie)

controller.wczytaj_dane()
gui.odswiez_liste_kin()
gui.odswiez_liste_pracownikow()
gui.odswiez_liste_klientow()
gui.odswiez_liste_seansow()
gui.odswiez_listy_rozwijalne_kin()
gui.odswiez_filtr_sieci_kin()

gui.root.mainloop()
import atexit
import os
import sys

from utils import gui, controller


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
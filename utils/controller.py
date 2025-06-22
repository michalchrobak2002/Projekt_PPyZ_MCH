import requests
from bs4 import BeautifulSoup

def pobierz_wspolrzedne(lokalizacja, czy_jest_internet=True):
    try:
        if not czy_jest_internet:
            return (52.23, 21.00)

        url = "https://pl.wikipedia.org/wiki/" + lokalizacja.replace(" ", "_")
        odpowiedz = requests.get(url, timeout=10)
        if odpowiedz.status_code == 200:
            soup = BeautifulSoup(odpowiedz.content, "html.parser")
            tagi_szerokosci = soup.select(".latitude")
            tagi_dlugosci = soup.select(".longitude")
            if len(tagi_szerokosci) >= 2 and len(tagi_dlugosci) >= 2:
                szerokosc = float(tagi_szerokosci[1].text.replace(",", "."))
                dlugosc = float(tagi_dlugosci[1].text.replace(",", "."))
                return (szerokosc, dlugosc)
        return (52.23, 21.00)
    except Exception as e:
        print(f"\nBłąd pobierania współrzędnych dla {lokalizacja}: {e}")
        return (52.23, 21.00)


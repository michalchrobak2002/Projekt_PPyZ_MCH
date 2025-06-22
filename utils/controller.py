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

import pandas as pd
import requests
import re
import locale
from bs4 import BeautifulSoup

# parser options
LEGES_KOSTEN = 125
ZINNEN_UIT_SPECIFICATIE = [
    "STANDAARD VOORZIEN"
]

# function to parse a product site of peters


def get_product_information(url: str) -> (bool, dict):
    locale.setlocale(locale.LC_ALL, '')

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    info = {}

    try:
        info["product_titel"] = soup.find(
            "h1", class_="product_title entry-title").text.strip()

        info["prijs_excl"] = float(locale.atof(re.findall("\d+\.\d+", soup.find(
            "span", class_="amount exvat").text.strip())[0]))
        info["prijs_incl"] = float(locale.atof(re.findall("([0-9]+[,.]+[0-9]+[,.]+[0-9]+)", soup.find(
            "span", class_="amount incvat").text.strip())[0]))

    except:
        return (False, "Kan de product titel, inclusief en/of exclusief prijs op de gegeven site niet vinden.")

    info['leges_kosten'] = 125

    # get first-specification
    try:
        specificaties = soup.find(
            "div", class_="first-specification").find("p").text.split("Opties")

        info['specificaties'] = specificaties[0].split("\n")
        info['specificaties'] = [re.sub(r'\W+', ' ', s)
                                 for s in info['specificaties'] if s.strip() != ""]

        # verwijder standaard zinnen
        info['specificaties'] = [s for s in info['specificaties'] if
                                 not any([substr in s.upper() for substr in ZINNEN_UIT_SPECIFICATIE])]

    except:
        return (False, "Kan de specificaties op de gegeven site niet vinden.")

    try:
        info['opties'] = specificaties[1].strip().split("\n")[1:]
    except:
        info['opties'] = []

    # dump table into Python dictionary
    try:
        table = soup.find("table", class_="specificaties")
        df = pd.read_html(str(table))[0]

        info['specificaties_table'] = df.set_index(0).to_dict('dict')[1]
        print(info['specificaties_table'])

    except:
        info['specificaties_table'] = {}
    return (True, info)

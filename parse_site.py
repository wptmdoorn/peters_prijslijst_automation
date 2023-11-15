import pandas as pd
import requests
from bs4 import BeautifulSoup


# function to parse a product site of peters
def get_product_information(url: str) -> dict:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    info = {}

    info["title"] = soup.find(
        "h1", class_="product_title entry-title").text.strip()

    info["amount_exvat"] = soup.find(
        "span", class_="amount exvat").text.strip()

    info["amount_incvat"] = soup.find(
        "span", class_="amount incvat").text.strip()

    # get first-specification
    specifications = soup.find(
        "div", class_="first-specification").find("p").text.split("Opties")

    info['specifications_first'] = specifications[0].strip().split("\n")
    info['specifications_second'] = specifications[1].strip().split("\n")[1:]

    # dump table into Python dictionary
    table = soup.find("table", class_="specificaties")
    df = pd.read_html(str(table))[0]

    info['specs_table'] = df.set_index(0).to_dict('dict')[1]

    return info

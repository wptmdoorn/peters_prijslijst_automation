
# from render_jinja import generate_pdf
import os
import sys
sys.path.append(os.getcwd())

# generate a fake product based on parse_site.py
product = {
    'product_titel': 'Peters Product',
    'opties_link': 'http://google.com',
    'opties_weergave_btw': 'Inclusief',
    'prijs_excl': 100,
    'prijs_incl': 121,
    'leges_kosten': 125,
    'specificaties': [f'Specificatie {i}' for i in range(1, 5)],
    'opties': [f'Optie {i}' for i in range(1, 3)],
    'specificaties_table': {'Specificatie 1': 'Waarde 1', 'Specificatie 2': 'Waarde 2', 'Specificatie 3': 'Waarde 3'}
}


def generate():
    from generate_pdf import generate_pdf
    generate_pdf(product)


generate()

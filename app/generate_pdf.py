from pathlib import Path
from jinja2 import Environment, FileSystemLoader, BaseLoader
import qrcode
import os
import re
import locale
import base64
import io
from datetime import datetime
from render_utils import html2pdf, format_price


def generate(info: dict, type: str, id: str) -> str:
    # setup locale
    locale.setlocale(locale.LC_ALL, "nl_NL")

    # generate filename
    _f = datetime.now().strftime('%Y%m%d_%H%M')

    clean_title = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]",
                         "-", info['product_titel'])
    clean_title = f"{clean_title}_{_f}"

    if info["opties_weergave_btw"] == "Inclusief":
        info["prijs_excl"] = info["prijs_excl"] * 1.21

    # Pas alle prijzen aan
    info["str_prijs_product"] = format_price(info['prijs_excl'])
    info["str_prijs_totaal"] = format_price(
        info['prijs_excl'] + info['leges_kosten'])
    info["leges_kosten_str"] = format_price(info['leges_kosten'])

    info["weergave_btw"] = "Prijs incl. BTW" if info["opties_weergave_btw"] == "Inclusief" else "Prijs excl. BTW"

    # generate QR code
    qrimg = qrcode.make(info['opties_link'])

    # Create buffer and save as PNG
    buffer = io.BytesIO()
    qrimg.save(buffer, 'PNG')

    # get the PNG-encoded image from buffer
    info["qrcode_base64"] = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Get File Content in String
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template(f'{id}/template.html')

    # Render HTML Template String
    render_template = template.render(
        info=info, css_text=Path(f'app/templates/{id}/template.css').read_text())

    # save files
    if not os.path.exists(f'output/{id}'):
        os.makedirs(f'output/{id}')

    with open(f"output/{id}/{clean_title}.html", "w", encoding='utf-8') as fh:
        fh.write(render_template)

    if type == "html":
        return os.path.join(os.getcwd(), 'output', id, f"{clean_title}.html")
    elif type == "pdf":
        html2pdf(f"output/{id}/{clean_title}.html",
                 f"output/{id}/{clean_title}.pdf")

        return os.path.join(os.getcwd(), 'output', id, f"{clean_title}.pdf")


def generate_custom(info: dict, type: str, html: str, css: str) -> str:
    # setup locale
    locale.setlocale(locale.LC_ALL, "nl_NL")

    # generate filename
    _f = datetime.now().strftime('%Y%m%d_%H%M')

    clean_title = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]",
                         "-", info['product_titel'])
    clean_title = f"{clean_title}_{_f}"

    if info["opties_weergave_btw"] == "Inclusief":
        info["prijs_excl"] = info["prijs_excl"] * 1.21

    # Pas alle prijzen aan
    info["str_prijs_product"] = format_price(info['prijs_excl'])
    info["str_prijs_totaal"] = format_price(
        info['prijs_excl'] + info['leges_kosten'])
    info["leges_kosten_str"] = format_price(info['leges_kosten'])

    info["weergave_btw"] = "Prijs incl. BTW" if info["opties_weergave_btw"] == "Inclusief" else "Prijs excl. BTW"

    # generate QR code
    qrimg = qrcode.make(info['opties_link'])

    # Create buffer and save as PNG
    buffer = io.BytesIO()
    qrimg.save(buffer, 'PNG')

    # get the PNG-encoded image from buffer
    info["qrcode_base64"] = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Get File Content in String
    template = Environment(loader=BaseLoader()).from_string(html)

    # Render HTML Template String
    render_template = template.render(
        info=info, css_text=css)

    # save files
    with open(f"output/{clean_title}.html", "w", encoding='utf-8') as fh:
        fh.write(render_template)

    if type == "html":
        return os.path.join(os.getcwd(), 'output', f"{clean_title}.html")
    elif type == "pdf":
        html2pdf(f"output/{clean_title}.html",
                 f"output/{clean_title}.pdf")

        return os.path.join(os.getcwd(), 'output', f"{clean_title}.pdf")

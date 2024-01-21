from pathlib import Path
import locale
import pdfkit
from pypdf import PdfWriter


def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'no-outline': None,
        'dpi': 300,
        'enable-local-file-access': None,
        'margin-top': '0.25in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        # "disable-smart-shrinking": None,
        # "zoom": 0.5
    }

    with open(html_path, encoding='utf-8') as f:
        pdfkit.from_file(f, pdf_path, options=options)

    pdf_writer = PdfWriter()
    pdf_writer.append(pdf_path, pages=(0, 1))

    with open(pdf_path, "wb") as fp:
        pdf_writer.write(fp)


def format_price(price: float) -> str:
    locale.setlocale(locale.LC_ALL, "nl_NL")
    return f"€ {locale.format('%.2f', price, grouping=True)}".replace(",00", ",--")

import locale
import pdfkit


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
        'margin-left': '0.25in'
    }
    with open(html_path, encoding='utf-8') as f:
        pdfkit.from_file(f, pdf_path, options=options)


def format_price(price: float) -> str:
    locale.setlocale(locale.LC_ALL, '')
    return f"€ {locale.format('%.2f', price, grouping=True)}".replace(",00", ",--")

from pathlib import Path
from parse_site import get_product_information
from jinja2 import Template, Environment, FileSystemLoader
from xhtml2pdf import pisa
import pdfkit
import os
from datetime import datetime


def _html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)


def generate_and_return_url(url: str) -> str:
    info = get_product_information(url)

    # Get File Content in String
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template_v1.html')

    # Render HTML Template String
    render_template = template.render(info=info)

    # save to file with current date and time
    _f = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open(f"output/file_{_f}.html", "w") as fh:
        fh.write(render_template)

    _html2pdf(f"output/file_{_f}.html",
              f"output/file_{_f}.pdf")

    return os.path.join(os.path.dirname(__file__), 'output', f'file_{_f}.pdf')

#!/usr/bin/env python3
from io import BytesIO
from pathlib import Path
from render_jinja import generate_and_return_url
import os

from nicegui import ui


@ui.page('/')
def home():

    def download_document(link: str):
        # check if valid URL

        print('called!')
        print(link)

        if "petersaanhangwagens.nl" not in link:
            ui.notify('Geen valide link - probeer opnieuw!')
        else:
            l = generate_and_return_url(link)
            print(l)
            return l

    with ui.card().classes('items-center fixed-center').style('min-width: 500px'):
        ui.image('logo.png').style('width: 60%;')
        ui.label('Maak je prijslijst!')

        link = ui.input('Product URL', placeholder='URL naar de productpagina').style(
            'width: 300px')

        ui.button('Download PDF', on_click=lambda: ui.download(
            download_document(link.value))).bind_visibility_from(link, 'value')


ui.run(title='Peters Prijslijst Generator', favicon="🚀", on_air=False)

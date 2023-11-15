#!/usr/bin/env python3
from render_jinja import generate_and_return_url
from nicegui import ui


@ui.page('/')
def home():
    """This function downloads a document from a given URL."""
    def download_document(link: str):
        # check if valid URL
        if "petersaanhangwagens.nl" not in link:
            ui.notify('Geen valide link - probeer opnieuw!')
        else:
            return generate_and_return_url(link)

    with ui.card().classes('items-center fixed-center').style('min-width: 500px'):
        ui.image('logo.png').style('width: 60%;')
        ui.label('Maak je prijslijst!')

        link = ui.input('Product URL', placeholder='URL naar de productpagina').style(
            'width: 300px')

        ui.button('Download PDF', on_click=lambda: ui.download(
            download_document(link.value))).bind_visibility_from(link, 'value')


ui.run(title='Peters Prijslijst Generator', favicon="🚀", on_air=False)

from nicegui import ui, app, Client
import os


def page(router) -> None:
    @router.page('/')
    def home_page(client: Client):
        def naar_bedrijf(id):
            if os.path.exists(f'app/templates/{id}'):
                ui.open(f'/prijslijst/bedrijf/{id}', new_tab=False)
            else:
                ui.notify(
                    'Bedrijf bestaat niet, weet u zeker dat u het juiste ID heeft gebruikt?', type='negative')

        client.layout.style(
            "background-image: url('/static/background.png'); background-size: cover;")

        with ui.column().classes('items-center fixed-center'):
            with ui.card().classes('items-center').style('min-width: 500px; max-width: 600px'):
                ui.label('''Welkom op de prijslijst generator van PyDoorn! Indien je reeds geabboneerd bent op onze service, kan je hieronder inloggen. 
                        Indien je nog geen abbonement hebt, kan je via onderstaande gegevens contact met ons opnemen.''')

                with ui.row().style('align-items: center;').props('vertical inline-label indicator-color="transparent"'):
                    bedrijfs_id = ui.input('Bedrijfs ID').on(
                        'keydown.enter', lambda: naar_bedrijf(bedrijfs_id.value))
                    ui.button('Inloggen').bind_visibility_from(
                        target_object=bedrijfs_id, target_name='value').on('click', lambda: naar_bedrijf(bedrijfs_id.value))

            with ui.card().classes('items-center').style('min-width: 500px; max-width: 600px'):
                ui.label(
                    'Heeft u vragen of zou u ook graag gebruik maken van onze technologie? Neem contact met ons op via')
                with ui.link('', 'mailto:info@pydoorn.nl', new_tab=True).style("textDecoration: inherit"):
                    ui.label("info@pydoorn.nl").style("color: red;    ")
                ui.label('We komen graag met u in contact!''').classes(
                    'text-grey-10')

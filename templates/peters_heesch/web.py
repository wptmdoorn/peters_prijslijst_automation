#!/usr/bin/env python3
from generate_pdf import generate_pdf
from nicegui import ui, app
import os
import validators
from .parser import get_product_information

ID = "peters_heesch"


def home(client):
    def reset_storage():
        # hard reset for now
        for k in app.storage.user:
            app.storage.user[k] = ''

    def retrieve_information(stepper):
        if not validators.url(app.storage.user['opties_link']):
            ui.notify(
                'Geen geldige link - probeer opnieuw met een juiste link.', type='negative')

        else:
            r = get_product_information(app.storage.user['opties_link'])

            if r[0]:
                for k, v in r[1].items():
                    app.storage.user[k] = v
                    stepper.next()
            else:
                ui.notify(r[1], type='negative')
                ui.notify(
                    'Probeer opnieuw met een juiste link. Indien dit het niet verhelpt, neem contact op met de ontwikkelaar.', type='negative')

    def retrieve_pdf():
        pdf_link = generate_pdf(app.storage.user)
        reset_storage()
        return pdf_link

    @ui.refreshable
    def show_laad():
        ui.input('Product URL', placeholder='URL naar de productpagina').style(
            'width: 300px').bind_value(app.storage.user, 'opties_link')

        with ui.stepper_navigation():
            ui.button('Laad').bind_visibility_from(
                app.storage.user, 'opties_link').on('click', lambda: (retrieve_information(stepper)))

    @ui.refreshable
    def show_opties():
        ui.number(label='Legeskosten', min=0, max=1000).classes('w-full').bind_value(
            app.storage.user, 'leges_kosten')

        ui.select(label='Weergave van BTW', options=['Exclusief', 'Inclusief'], value='Exclusief').bind_value(
            app.storage.user, 'opties_weergave_btw').classes('w-full')

        with ui.stepper_navigation():
            ui.button('Genereer').bind_visibility_from(
                app.storage.user, 'opties_link').on('click', lambda: (stepper.next()))
            ui.button('Terug', on_click=stepper.previous).props('flat')

    @ui.refreshable
    def show_download(stepper):
        with ui.stepper_navigation():
            ui.button('Download', on_click=lambda: (ui.download(
                retrieve_pdf())))
            ui.button('Reset', on_click=lambda: stepper.set_value(
                'Laad product')).props('flat')

    reset_storage()
    client.layout.style(
        "background-image: url('/../../static/background.png'); background-size: cover;")
    app.add_static_files('/../../static', 'static')
    ui.page_title('Peters Aanhangers - Maak je prijslijst!')

    with ui.card().classes('items-center fixed-center').style('min-width: 500px'):
        ui.image(f'templates/{ID}/logo.png').style('width: 60%;')
        ui.label('Maak je prijslijst!')

        with ui.tabs() as tabs:
            ui.tab('h', label='Prijslijsten', icon='home')
            ui.tab('a', label='Coming soon..', icon='info')

        with ui.tab_panels(tabs, value='h').classes('w-full'):
            with ui.tab_panel('h'):

                with ui.stepper().props('vertical').classes('w-full') as stepper:
                    with ui.step('Laad product').classes('w-full'):
                        show_laad()

                    with ui.step('Selecteer opties').classes('w-full'):
                        show_opties()

                    with ui.step('Download PDF'):
                        show_download(stepper)

            with ui.tab_panel('a'):
                ui.label('Coming soon..')

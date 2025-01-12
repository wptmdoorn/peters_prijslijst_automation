#!/usr/bin/env python3
from generate_pdf import generate
from nicegui import ui, app
import os
import validators
from .parser import get_product_information

ID = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
PRODUCT_VERSIE = 'demo'


def home(client):
    def reset_storage():
        # hard reset for now
        for k in app.storage.user:
            app.storage.user[k] = ''

        try:
            app.storage.user['stat_aantal_prijslijsten'] = int(len(
                os.listdir(f'output/{ID}')) / 2)
        except:
            app.storage.user['stat_aantal_prijslijsten'] = 0

    def retrieve_information(stepper):
        if PRODUCT_VERSIE == 'demo' and app.storage.user['stat_aantal_prijslijsten'] >= 25:
            ui.notify(
                '''Je hebt de limiet van 25 prijslijsten bereikt. 
                Neem contact op voor verdere opties.''', type='negative')

        elif not validators.url(app.storage.user['opties_link']):
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
        pdf_link = generate(app.storage.user, type='pdf', id=ID)
        reset_storage()
        show_balk.refresh()
        return pdf_link

    @ui.refreshable
    def show_balk():
        n = app.storage.user['stat_aantal_prijslijsten']

        if PRODUCT_VERSIE == 'betaald':
            with ui.column().classes('w-full items-center'):
                with ui.element('div').classes(
                    'p-2 bg-green-100 justify-center').style(
                        'justify-content: center; height: 40px; width: 300px; border-radius: 25px'):
                    ui.label('betaalde versie').classes('text-center')

        elif PRODUCT_VERSIE == 'demo':
            _bg = 'bg-orange-100' if n < 25 else 'bg-red-100'

            with ui.column().classes('w-full items-center'):
                with ui.element('div').classes(
                    f'p-2 {_bg} justify-center').style(
                        f'justify-content: center; height: 40px; width: {(200+((n/25)*100))}px; border-radius: 25px'):
                    ui.label(f'demo - {n}/25 producten').classes('text-center')

    @ui.refreshable
    def show_laad():
        ui.input('Product URL', placeholder='URL naar de productpagina').style(
            'width: 300px').bind_value(app.storage.user, 'opties_link')

        with ui.stepper_navigation():
            ui.button('Laad').bind_visibility_from(
                app.storage.user, 'opties_link').on('click', lambda: (retrieve_information(stepper)))

    @ui.refreshable
    def show_opties():
        ui.number(label='Legeskosten (BTW vrij)', min=0, max=1000).classes('w-full').bind_value(
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
        "background-image: url('/static/background.png'); background-size: cover;")
    ui.page_title('Peters Aanhangers - Maak je prijslijst!')

    with ui.card().classes('items-center fixed-center').style('min-width: 500px'):
        ui.image(f'app/templates/{ID}/logo.png').style('width: 60%;')
        ui.label(f'Maak je prijslijst!')

        with ui.tabs() as tabs:
            ui.tab('h', label='Prijslijsten', icon='home')

        with ui.tab_panels(tabs, value='h').classes('w-full'):
            with ui.tab_panel('h'):
                with ui.card().classes('w-full'):
                    show_balk()

                    with ui.stepper().props('vertical').classes('w-full') as stepper:
                        with ui.step('Laad product').classes('w-full'):
                            show_laad()

                        with ui.step('Selecteer opties').classes('w-full'):
                            show_opties()

                        with ui.step('Download PDF'):
                            show_download(stepper)

            with ui.tab_panel('a'):
                ui.label('Coming soon..')

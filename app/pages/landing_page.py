from nicegui import ui


def page(router) -> None:
    @router.page('/')
    def home(client):
        client.layout.style(
            "background-image: url('/static/background.png'); background-size: cover;")
        ui.page_title('PyDoorn')

        with ui.column().classes('w-full items-center'):
            ui.image('/static/logo 1000x400.png').classes('w-1/4')
            ui.html('Software producten voor het MKB &#128640;').classes(
                'text-2xl items-center')
            with ui.row().classes('w-1/2'):
                ui.separator().props("color=green")

        with ui.row().classes('w-full justify-center q-pa-md row items-start q-gutter-md'):
            with ui.card().classes('text-center items-center col-xs-12 col-sm-6 col-md-3 col-lg-3 transform transition duration-500 bg-white-500 hover:bg-green-500 hover:scale-105').on('click', lambda: ui.open('/prijslijst')):
                ui.image(
                    '/static/landing_prijslijst.jpeg').classes('rounded-sm')
                ui.markdown('#### Automatische prijslijsten')
                ui.label('''Moet u altijd handmatig uw prijslijsten maken?
                         Bent u ook op meerdere plekken uw prijzen aan het bijhouden?
                         Wij hebben de oplossing voor u!
                         Wij maken software die automatisch uw prijslijsten genereert.''')

            with ui.card().classes('text-center items-center col-xs-12 col-sm-6 col-md-3 col-lg-3 transform duration-500 bg-grey-5 hover:bg-green hover:scale-105').on('click', lambda: ui.open('mailto:info@pydoorn.nl')):
                ui.image(
                    '/static/landing_maat.jpeg').classes('rounded-5xl overflow-hidden')
                ui.markdown('#### Uw software op maat?')
                ui.html('''Heeft u een specifieke wens voor uw software?
                         Wij maken software op maat voor u.
                         Wij hebben ervaring met het maken van software voor het MKB.
                         Klik hier of neem contact op via <a href="mailto:info@pydoorn.nl">info@pydoorn.nl</a>
                        voor een vrijblijvend gesprek!''')

        with ui.column().classes('w-full items-center'):
            with ui.row().classes('w-1/2'):
                ui.separator().props("color=green")

            ui.html('''PyDoorn | KVK 93043252 | info@pydoorn.nl | 
                    <a href="/static/algemene_voorwaarden.pdf">Algemene Voorwaarden</a> | 
                    <a href="/static/privacy_verklaring.pdf">Privacy verklaring</a>''').classes(
                'text-2s text-grey')

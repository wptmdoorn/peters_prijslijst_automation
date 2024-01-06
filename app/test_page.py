from nicegui import ui
from generate_pdf import generate_custom

product = {
    'product_titel': 'Peters Product',
    'opties_link': 'http://google.com',
    'opties_weergave_btw': 'Inclusief',
    'prijs_excl': 100,
    'prijs_incl': 121,
    'leges_kosten': 125,
    'specificaties': [f'Specificatie {i}' for i in range(1, 17)],
    'opties': [f'Optie {i}' for i in range(1, 9)],
    # 8 specificaties
    'specificaties_table': {'Specificatie 1': 'Waarde 1', 'Specificatie 2': 'Waarde 2', 'Specificatie 3': 'Waarde 3', 'Specificatie 4': 'Waarde 4', 'Specificatie 5': 'Waarde 5',
                            'Specificatie 6': 'Waarde 6', 'Specificatie 7': 'Waarde 7', 'Specificatie 8': 'Waarde 8', 'Specificatie 9': 'Waarde 9', 'Specificatie 10': 'Waarde 10',
                            'Specificatie 11': 'Waarde 11'},
}


def create() -> None:
    def render(html: str, css: str, type: str) -> str:
        return generate_custom(product, type, html, css)

    @ui.page('/test/render')
    def test_render_page():
        with ui.card().classes('items-center').style('min-width: 500px; max-width: 600px'):
            html = ui.textarea().classes('w-full')
            css = ui.textarea().classes('w-full')
            html_button = ui.button('Render HTML').on(
                'click', lambda: (ui.download(render(html.value, css.value, 'html'))))

            pdf_button = ui.button('Render PDF').on(
                'click', lambda: (ui.download(render(html.value, css.value, 'pdf'))))
"""
This is the main application file for our NiceGUI
application that will be used to generate PDF files.
It serves as the homepage but also as the router to all the individual company pages.
"""

from pages import home, test, bedrijf, landing_page
from nicegui import ui, app, APIRouter

app.add_static_files('/static', 'static')
router_landing = APIRouter()
router = APIRouter(prefix='/prijslijst')


home.page(router)
bedrijf.page(router)
test.page(router)

landing_page.page(router_landing)

app.include_router(router)
app.include_router(router_landing)

# fulfill
ui.run(title='Prijslijst Generator - PyDoorn', host='0.0.0.0', port=8080,
       favicon="🚀", on_air=False, storage_secret='xxxxx', dark=False)

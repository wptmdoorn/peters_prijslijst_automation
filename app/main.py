"""
This is the main application file for our NiceGUI
application that will be used to generate PDF files.
It serves as the homepage but also as the router to all the individual company pages.
"""

from pages import home, test, bedrijf
from nicegui import ui

home.page()
bedrijf.page()
test.page()

# fulfill
ui.run(title='Prijslijst Generator - PyDoorn', host='0.0.0.0', port=8080,
       favicon="🚀", on_air=False, storage_secret='xxxxx', dark=False)

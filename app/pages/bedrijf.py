
from nicegui import ui, Client, App
import os
import importlib
from fastapi.responses import RedirectResponse


def page() -> None:
    @ui.page('/bedrijf/{id}')
    def bedrijfs_pagina(id, client: Client):
        print(os.getcwd())
        if os.path.exists(f'app/templates/{id}'):
            bedrijfs_module = importlib.import_module(f'templates.{id}.web')

            return bedrijfs_module.home(client)

        else:
            return RedirectResponse('/')

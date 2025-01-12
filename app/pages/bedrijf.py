
from nicegui import ui, Client, App
import os
import importlib
from fastapi.responses import RedirectResponse


def page(router) -> None:
    @router.page('/bedrijf/{id}')
    def bedrijfs_pagina(id, client: Client):

        if os.path.exists(f'app/templates/{id}'):
            bedrijfs_module = importlib.import_module(f'templates.{id}.web')

            return bedrijfs_module.home(client)

        else:
            return RedirectResponse('/')

import flet as ft
import controller as c
import view as v

def main(page: ft.Page):
    # Setup model, view, control according to MVC pattern
    view = v.View(page)
    controller = c.SpellChecker(view)
    view.setController(controller)
    view.add_content()  # Add this call here, ensure it's only called once

ft.app(target=main)

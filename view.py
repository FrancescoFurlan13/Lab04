import flet as ft


class View:
    def __init__(self, page: ft.Page):
        # Page setup
        self.page = page
        self.page.title = "TdP 2024 - Lab 04 - SpellChecker ++"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(
            color_scheme_seed="blue"
        )

        # Controller
        self.__controller = None

        # UI elements
        self.__title = ft.Text("TdP 2024 - Lab 04 - SpellChecker ++", size=24, color="blue")
        self.__theme_switch = ft.Switch(label="Light theme", on_change=self.theme_changed)

        # Dropdowns for language and modality
        self.__language_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("italian", "Italiano"),
                ft.dropdown.Option("english", "Inglese"),
                ft.dropdown.Option("spanish", "Spagnolo")
            ],
            label="Seleziona la lingua",
            on_change=self.language_selected
        )

        self.__modality_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("default", "Default"),
                ft.dropdown.Option("linear", "Linear"),
                ft.dropdown.Option("dichotomic", "Dichotomic")
            ],
            label="Seleziona la modalità di ricerca",
            on_change=self.modality_selected
        )

        # Text field for sentence input
        self.__sentence_input = ft.TextField(label="Inserisci la tua frase", expand=True)

        # Button for spell check
        self.__spell_check_button = ft.ElevatedButton(text="Spell Check", on_click=self.handle_spell_check)

        # Text for result output
        self.__result_text = ft.Text()

        # ListView for detailed results
        self.__list_view = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    def add_content(self):
        """Function that creates and adds the visual elements to the page. It also updates the page accordingly."""
        self.page.add(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[self.__title, self.__theme_switch],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        controls=[self.__language_dropdown],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row(
                        controls=[self.__modality_dropdown, self.__sentence_input, self.__spell_check_button],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row(
                        controls=[self.__result_text],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    self.__list_view
                ]
            )
        )
        self.page.update()

    def update(self):
        self.page.update()

    def setController(self, controller):
        self.__controller = controller

    def theme_changed(self, e):
        """Function that changes the color theme of the app, when the corresponding switch is triggered"""
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.__theme_switch.label = (
            "Light theme" if self.page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        self.page.update()

    def language_selected(self, e):
        self.__result_text.value = f"Lingua selezionata: {self.__language_dropdown.value}"
        self.update()

    def modality_selected(self, e):
        self.__result_text.value = f"Modalità di ricerca selezionata: {self.__modality_dropdown.value}"
        self.update()

    def handle_spell_check(self, e):
        if self.__controller:
            language = self.__language_dropdown.value
            modality = self.__modality_dropdown.value
            sentence = self.__sentence_input.value
            if not language or not modality or not sentence:
                self.__result_text.value = "Per favore, compila tutti i campi."
            else:
                result, time_taken = self.__controller.handleSentence(sentence, language, modality)
                self.__list_view.controls.clear()  # Clear previous results
                self.__list_view.controls.append(ft.Text(
                    f"Frase inserita: {sentence}\n"
                    f"Parole errate: {result}\n"
                    f"Tempo richiesto dalla ricerca: {time_taken} secondi"
                ))
                self.__sentence_input.value = ""
            self.update()

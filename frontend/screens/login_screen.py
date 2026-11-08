import flet as ft
from api_client import api


class LoginScreen:
    def __init__(self, page: ft.Page, on_success, on_register_click):
        self.page = page
        self.on_success = on_success
        self.on_register_click = on_register_click
        
        self.username_field = ft.TextField(
            label="Логин",
            width=300,
            border=ft.InputBorder.OUTLINE,
            autofocus=True
        )
        self.password_field = ft.TextField(
            label="Пароль",
            password=True,
            can_reveal_password=True,
            width=300,
            border=ft.InputBorder.OUTLINE
        )
        self.status_text = ft.Text("", color=ft.Colors.RED, size=14)
        self.loading_indicator = ft.ProgressRing(visible=False)

    def build(self):
        async def login_click(e):
            self.status_text.value = ""
            self.loading_indicator.visible = True
            self.page.update()

            username = self.username_field.value
            password = self.password_field.value

            if not username or not password:
                self.status_text.value = "Заполните все поля!"
                self.loading_indicator.visible = False
                self.page.update()
                return

            try:
                user_data = await api.login(username, password)
                self.on_success(user_data)
            except Exception as ex:
                self.status_text.value = f"Ошибка: {str(ex)}"
                self.loading_indicator.visible = False
                self.page.update()

        def register_click(e):
            self.on_register_click()

        return ft.Column(
            [
                ft.Text("ServiceBook", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ft.Text("Вход в систему", size=16, color=ft.Colors.GREY_600),
                ft.Container(height=20),
                self.username_field,
                self.password_field,
                self.status_text,
                self.loading_indicator,
                ft.ElevatedButton(
                    "Войти",
                    on_click=login_click,
                    width=300,
                    height=45,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE
                    )
                ),
                ft.TextButton(
                    "Нет аккаунта? Зарегистрироваться",
                    on_click=register_click,
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE
                    )
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
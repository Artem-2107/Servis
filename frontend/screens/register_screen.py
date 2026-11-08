import flet as ft
from api_client import api

class RegisterScreen:
    def __init__(self, page: ft.Page, on_success, on_login_click):
        self.page = page
        self.on_success = on_success
        self.on_login_click = on_login_click
        
        self.username = ft.TextField(
            label="Придумайте логин", 
            prefix_icon=ft.Icons.PERSON, 
            autofocus=True
        )
        self.password = ft.TextField(
            label="Придумайте пароль (мин. 6 символов)", 
            prefix_icon=ft.Icons.LOCK, 
            password=True, 
            can_reveal_password=True
        )
        self.password_confirm = ft.TextField(
            label="Повторите пароль", 
            prefix_icon=ft.Icons.LOCK, 
            password=True, 
            can_reveal_password=True
        )
        
        # Поле выбора роли
        self.role_dropdown = ft.Dropdown(
            label="Выберите роль",
            options=[
                ft.dropdown.Option("admin", "Администратор"),
                ft.dropdown.Option("manager", "Мастер-приемщик"),
                ft.dropdown.Option("accountant", "Бухгалтер"),
            ],
            value="manager",  # По умолчанию
            prefix_icon=ft.Icons.SHIELD,
        )
        
        self.error_text = ft.Text("", color=ft.Colors.RED_400, size=12)
        self.loading = ft.ProgressRing(visible=False, width=20, height=20)

    def build(self):
        return ft.Container(
            width=400, 
            padding=40, 
            border_radius=12, 
            bgcolor=ft.Colors.GREY_800,
            content=ft.Column([
                ft.Icon(ft.Icons.PERSON_ADD, size=64, color=ft.Colors.GREEN),
                ft.Text("Регистрация", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Создайте новый аккаунт", size=14, color=ft.Colors.GREY, text_align=ft.TextAlign.CENTER),
                ft.Divider(height=24, color=ft.Colors.TRANSPARENT),
                self.username,
                self.password,
                self.password_confirm,
                self.role_dropdown,
                self.error_text,
                ft.ElevatedButton(
                    "Зарегистрироваться", 
                    width=200, 
                    on_click=self._register, 
                    bgcolor=ft.Colors.GREEN, 
                    color=ft.Colors.WHITE
                ),
                self.loading,
                ft.Divider(height=16, color=ft.Colors.TRANSPARENT),
                ft.TextButton("Назад ко входу", on_click=self.on_back_to_login),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
        )

    def on_back_to_login(self, e):
        """Обработчик кнопки 'Назад ко входу' - принимает event"""
        self.on_login_click()

    def _register(self, e):
        self.error_text.value = ""
        self.loading.visible = True
        self.page.update()

        async def do_register():
            try:
                # Валидация
                if not self.username.value.strip():
                    raise ValueError("Введите логин")
                if not self.password.value:
                    raise ValueError("Введите пароль")
                if len(self.password.value) < 6:
                    raise ValueError("Пароль должен содержать минимум 6 символов")
                if self.password.value != self.password_confirm.value:
                    raise ValueError("Пароли не совпадают")
                if not self.role_dropdown.value:
                    raise ValueError("Выберите роль")

                # Регистрация (роль в нижнем регистре!)
                await api.register(
                    username=self.username.value.strip(),
                    password=self.password.value,
                    email=f"{self.username.value.strip()}@service.ru",
                    full_name=self.username.value.strip(),
                    role=self.role_dropdown.value  # 'admin', 'manager' или 'accountant'
                )
                
                self.on_success()
            except Exception as ex:
                self.error_text.value = f"Ошибка: {str(ex)}"
            finally:
                self.loading.visible = False
                self.page.update()

        self.page.run_task(do_register)
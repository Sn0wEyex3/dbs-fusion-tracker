# views/login_view.py
import flet as ft
from database import get_or_create_profile

def LoginView(page: ft.Page, on_login_success) -> ft.Control:
    """Baut den reibungslosen Device-ID Onboarding-Screen."""

    title = ft.Text("DBS Fusion World", size=26, weight=ft.FontWeight.BOLD, color="orange")
    subtitle = ft.Text("Wie lautet dein Spielername für das Event?", size=14, color="grey")

    username_input = ft.TextField(label="Dein Spielername", hint_text="z.B. GokuFan99")
    status_text = ft.Text("", size=14)

    def handle_start(e):
        username = username_input.value.strip() if username_input.value else ""
        if len(username) < 3:
            status_text.value = "⚠️ Bitte einen Namen mit mindestens 3 Zeichen eingeben!"
            status_text.color = "orange"
            page.update()
            return

        pseudo_device_id = f"event-device-{username.lower()}"
        success, message = get_or_create_profile(username, pseudo_device_id)
        
        if success:
            page.session.store.set("username", username)
            on_login_success()
        else:
            status_text.value = f"❌ {message}"
            status_text.color = "red"
            page.update()

    start_btn = ft.Button("Loslegen & Stats tracken", icon="check", on_click=handle_start)

    return ft.Column(
        controls=[
            title,
            subtitle,
            ft.Divider(),
            username_input,
            start_btn,
            ft.Container(height=10),
            status_text
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER
    )

# main.py
import flet as ft
from views.match_view import MatchView
from views.profile_view import ProfileView

def main(page: ft.Page):
    # App-Einstellungen
    page.title = "DBS Fusion World Tracker"
    page.window.width = 400
    page.window.height = 750
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"

    def switch_tab(e):
        """Wechselt den Screen je nach geklicktem Icon in der Navigation Bar."""
        page.controls.clear()
        if e.control.selected_index == 0:
            page.add(MatchView(page))
        elif e.control.selected_index == 1:
            page.add(ProfileView(page))
        page.update()

    def show_main_app():
        """Baut die Haupt-App mit Navigation Bar nach erfolgreichem Login auf."""
        page.controls.clear()
        
        # Navigation Bar unten anheften (mit sauberen String-Icons und String-Labels)
        page.navigation_bar = ft.NavigationBar(
            selected_index=0,      
            bgcolor="#1E1E1E",     
            indicator_color="orange",
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, label="Eintragen"),
                ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED, label="Profil"),
            ],
            on_change=switch_tab
        )
        
        # Standardmäßig den ersten Tab (Match eintragen) laden
        page.add(MatchView(page))
        page.update()

    def show_login_view():
        """Prüft beim Start, ob bereits ein Username da ist. Wenn nicht, Login anzeigen."""
        page.controls.clear()
        page.navigation_bar = None 
        
        # Prüfen, ob im Arbeitsspeicher (Session) schon ein Name hinterlegt ist
        if page.session.store.get("username"):
            show_main_app()
        else:
            from views.login_view import LoginView
            page.add(LoginView(page, on_login_success=show_main_app))
            page.update() 

    # App startet immer zuerst mit dem Login-Prüfer
    show_login_view()
    page.update()

if __name__ == "__main__":
    ft.run(main)

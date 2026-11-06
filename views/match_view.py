import flet as ft
from database import get_leaders, save_match_data, get_matchup_stats

def MatchView(page: ft.Page) -> ft.Control:
    """Baut die Benutzeroberflaeche fuer das Match-Eingabeformular."""
    
    # Vorschläge für AutoComplete aufbereiten
    leader_suggestions = [
        ft.AutoCompleteSuggestion(key=leader, value=leader) 
        for leader in get_leaders()
    ]

    # UI-Komponenten
    title = ft.Text("Match eintragen", size=24, weight=ft.FontWeight.BOLD, color="orange")

    format_dropdown = ft.Dropdown(
        label="Format",
        options=[
            ft.dropdown.Option("Digital Client"),
            ft.dropdown.Option("Local / Store Tournament"),
            ft.dropdown.Option("Store Regional"),
            ft.dropdown.Option("Regional"),
            ft.dropdown.Option("Ultimate Battle"),
            ft.dropdown.Option("Pre-Release"),
            ft.dropdown.Option("Just for Fun"),
            ft.dropdown.Option("Finals"),
            ft.dropdown.Option("Grand Finals"),
            ft.dropdown.Option("Last Chance Qualifier"),


        ],
        value="Digital Client"
    )

    matchup_stats_text = ft.Text("", size=13, color="blue", italic=True)

    def update_stats (e):
        if my_leader.value and opp_leader.value:
            stats = get_matchup_stats(my_leader.value, opp_leader.value)
            matchup_stats_text.value = stats
        else:
            matchup_stats_text.value = ""
        page.update()

    # 2. Decks / Leader mit separaten Labels fuer die Fehlerfreiheit
    my_leader_label = ft.Text("Eigener Leader:", size=14, color="grey")
    my_leader = ft.AutoComplete(
        suggestions=leader_suggestions
    )

    opp_leader_label = ft.Text("Gegnerischer Leader:", size=14, color="grey")
    opp_leader = ft.AutoComplete(
        suggestions=leader_suggestions
    )

    # 3. Switches & Spieldaten
    dice_switch = ft.Switch(label="Dice roll win?", value=True)
    first_switch = ft.Switch(label="Going First (Anfangshand)?", value=True)
    win_switch = ft.Switch(label="Gewonnen (Win)?", value=True)
    mulligan_switch = ft.Switch(label="Mulligan?", value=True)


    turns_input = ft.TextField(label="Anzahl Turns", keyboard_type=ft.KeyboardType.NUMBER, value="5")
    key_card_input = ft.TextField(label="Key Card / MVP", hint_text="z.B. SCR Gohan")
    notes_input = ft.TextField(label="Notizen / Spielfehler", multiline=True, min_lines=3)

    status_text = ft.Text("", color="green", weight=ft.FontWeight.BOLD)

    # Event-Handler fuer den Speichern-Button
    def on_save_clicked(e):
        match_data = {
            "format": format_dropdown.value,
            "my_leader": my_leader.value,
            "opp_leader": opp_leader.value,
            "dice": dice_switch.value,
            "first": first_switch.value,
            "win": win_switch.value,
            "mulligan": mulligan_switch.value,
            "turns": turns_input.value,
            "key_card": key_card_input.value,
            "notes": notes_input.value,
            "username": page.session.store.get("username")
        }
        
        # Aufruf der Datenbank-Funktion
        if save_match_data(match_data):
            status_text.value = f"✅ Match gespeichert: {my_leader.value} vs {opp_leader.value}"
            status_text.color = "green"
        else:
            status_text.value = "❌ Fehler beim Speichern des Matches."
            status_text.color = "red"
        
        page.update()

    # FIX: Use safe string identifier for icon instead of strict variable reference
    save_btn = ft.Button("Match Speichern", icon="save", on_click=on_save_clicked)

    # Zusammenbau des Layout-Containers für diesen Screen
    return ft.Column(
        controls=[
            title,
            ft.Divider(),
            format_dropdown,
            my_leader_label,
            my_leader,
            opp_leader_label,
            opp_leader,
            matchup_stats_text,
            dice_switch,
            first_switch,
            win_switch,
            mulligan_switch,
            turns_input,
            key_card_input,
            notes_input,
            ft.Container(height=10),
            save_btn,
            status_text
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE
    )

# views/profile_view.py
import flet as ft
from database import get_user_matches

def ProfileView(page: ft.Page) -> ft.Control:
    """Baut das Profil- und Statistik-Dashboard auf."""
    
    username = page.session.store.get("username") or "Unbekannter Spieler"
    
    # Matches aus Supabase laden
    matches = get_user_matches(username)
    
    # Statistiken berechnen
    total_games = len(matches)
    wins = sum(1 for m in matches if m.get("win") is True)
    losses = total_games - wins
    winrate = (wins / total_games * 100) if total_games > 0 else 0.0

    # Most Played Leader ermitteln
    leader_counts = {}
    for m in matches:
        leader = m.get("my_leader")
        if leader:
            leader_counts[leader] = leader_counts.get(leader, 0) + 1
            
    most_played = max(leader_counts, key=leader_counts.get) if leader_counts else "Noch keine Spiele"

    # UI-Komponenten
    title = ft.Text(f"Profil: {username}", size=24, weight=ft.FontWeight.BOLD, color="orange")
    
    # Statistik-Karten
    stats_card = ft.Container(
        content=ft.Column([
            ft.Text("📊 Deine Gesamtstatistik", size=16, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Spiele gesamt: {total_games}"),
            ft.Text(f"Bilanz (Wins / Losses): {wins}W - {losses}L"),
            ft.Text(f"Overall Winrate: {winrate:.1f}%", weight=ft.FontWeight.BOLD, color="green" if winrate >= 50 else "red"),
            ft.Text(f"Most Played Leader: {most_played}"),
        ]),
        padding=15,
        bgcolor="#1E1E1E",
        border_radius=10,
    )

    history_title = ft.Text("📜 Match-Historie", size=18, weight=ft.FontWeight.BOLD)

    # Liste der Matches aufbauen
    match_list = ft.ListView(expand=1, spacing=10, padding=10)
    
    if not matches:
        match_list.controls.append(ft.Text("Bisher noch keine Matches eingetragen.", color="grey", italic=True))
    else:
        for m in matches:
            result_text = "🟢 WIN" if m.get("win") else "🔴 LOSS"
            result_color = "green" if m.get("win") else "red"
            
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{m.get('my_leader')} vs {m.get('opp_leader')}", weight=ft.FontWeight.BOLD),
                        ft.Text(result_text, color=result_color, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Format: {m.get('format')} | Turns: {m.get('turns')}", size=12, color="grey"),
                    ft.Text(f"Notizen: {m.get('notes')}", size=12, italic=True) if m.get('notes') else ft.Container()
                ]),
                padding=10,
                bgcolor="#2A2A2A",
                border_radius=8
            )
            match_list.controls.append(card)

    return ft.Column(
        controls=[
            title,
            stats_card,
            ft.Divider(),
            history_title,
            match_list
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE
    )

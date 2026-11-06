# database.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Supabase-Client initialisieren, falls Credentials vorhanden sind
if url and key:
    supabase: Client = create_client(url, key)
else:
    supabase = None

# Offizielle Leader-Liste für die Vorschläge (AutoComplete)
LEADERS = [
    "FB01-001 Son Goku"
    "Fb01-002 Beerus"
    "FB01-035 Goku Black"
]

def get_leaders():
    """Gibt die Liste aller verfügbaren Leader zurück."""
    return LEADERS

def get_or_create_profile(username: str, device_id: str) -> tuple[bool, str]:
    """Prüft oder erstellt ein Profil basierend auf der Geräte-ID und dem Usernamen."""
    if not supabase:
        return False, "Keine Datenbankverbindung."
    
    try:
        # 1. Prüfen, ob die Device-ID schon registriert ist
        existing = supabase.table("profiles").select("*").eq("device_id", device_id).execute()
        if existing.data:
            return True, "Willkommen zurück!"

        # 2. Prüfen, ob der Username bereits vergeben ist
        name_check = supabase.table("profiles").select("*").eq("username", username).execute()
        if name_check.data:
            return False, "Dieser Username ist leider schon vergeben."

        # 3. Neues Profil in Supabase anlegen
        profile_data = {
            "device_id": device_id,
            "username": username
        }
        supabase.table("profiles").insert(profile_data).execute()
        return True, "Profil erfolgreich erstellt!"
        
    except Exception as e:
        return False, str(e)

def save_match_data(match_data: dict) -> bool:
    """Speichert ein Match in der Supabase-Tabelle 'matches'."""
    if not supabase:
        print("❌ Keine Verbindung zu Supabase vorhanden.")
        return False

    try:
        response = supabase.table("matches").insert(match_data).execute()
        print("✅ Match erfolgreich in Supabase gespeichert:", response.data)
        return True
    except Exception as e:
        print(f"❌ Fehler beim Speichern in Supabase: {e}")
        return False

def get_user_matches(username: str) -> list:
    """Lädt alle gespeicherten Matches eines bestimmten Nutzers aus Supabase."""
    if not supabase:
        return []
    
    try:
        response = supabase.table("matches") \
            .select("*") \
            .eq("username", username) \
            .order("created_at", desc=True) \
            .execute()
        return response.data
    except Exception as e:
        print(f"❌ Fehler beim Laden der Matches: {e}")
        return []

def get_matchup_stats(my_leader: str, opp_leader: str) -> str:
    """Fragt in Supabase alle vergangenen Matches ab und berechnet die Winrate für das Matchup."""
    if not supabase or not my_leader or not opp_leader:
        return ""

    try:
        response = supabase.table("matches") \
            .select("win") \
            .eq("my_leader", my_leader) \
            .eq("opp_leader", opp_leader) \
            .execute()
        
        matches = response.data
        total_games = len(matches)

        if total_games == 0:
            return f"📊 Bisher keine Matches: {my_leader} vs {opp_leader}"

        wins = sum(1 for match in matches if match.get("win") is True)
        losses = total_games - wins
        winrate = (wins / total_games) * 100

        return f"📊 Bilanz vs {opp_leader}: {wins}W - {losses}L ({winrate:.1f}% Winrate)"

    except Exception as e:
        print(f"❌ Fehler bei Matchup-Stats Abfrage: {e}")
        return ""

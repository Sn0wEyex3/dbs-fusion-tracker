# database.py
import os

# Versuche dotenv zu laden, fange den Fehler ab, falls das Modul auf dem Server fehlt
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from supabase import create_client, Client

# Lade Umgebungsvariablen (greift auf Render-Environment oder lokale .env zu)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if url and key:
    supabase: Client = create_client(url, key)
else:
    supabase = None

# Offizielle Leader-Liste (für AutoComplete und Vorschläge)
LEADERS = [
    "FS01-01 Son Goku",
    "FS02-01 Vegeta",
    "FS03-01 Broly",
    "FS04-01 Frieza",
    "FS05-01 Bardock",
    "FS06-01 Son Goku(Mini)",
    "FS07-01 Vegeta(Mini)",
    "FS08-01 Vegeta(Mini) Super Saiyan 3",
    "FS09-01 Shallot",
    "FS10-01 Giblet",
    "FS11-01 Son Goku Super Saiyan 3",
    "FS12-01 Son Goku",
    "FB01-001 Son Goku",
    "FB01-002 Beerus",
    "FB01-035 Goku Black",
    "FB01-036 Trunks : Future",
    "FB01-070 Android 17",
    "FB01-071 Son Gohan : Childhood",
    "FB01-104 Ginyu",
    "FB01-105 Cooler",
    "FB02-001 Son Goku(ToP)",
    "FB02-036 Zamasu : Fused",
    "FB02-070 Cell",
    "FB02-105 Vegeta Y",
    "FB03-001 Jiren",
    "FB03-027 Son Goku",
    "FB03-053 Piccolo",
    "FB03-078 Babidi / Buu",
    "FB03-104 Son Goku : GT",
    "FB04-001 Son Goku",
    "FB04-026 Son Gohan : Adolescence",
    "FB04-051 Vegeta",
    "FB04-077 Majin Buu : Evil",
    "FB04-103 Baby Vegeta",
    "FB05-001 Son Goku (Mini) : DA",
    "FB05-025 Vegito",
    "FB05-049 Son Goku",
    "FB05-072 Janemba",
    "FB05-095 Gogeta",
    "FB06-001 Android 18",
    "FB06-025 Son Goku : Childhood",
    "FB06-048 Broly : BR",
    "FB06-071 King Gomah : DA",
    "FB06-095 King Piccolo",
    "SB01-001 Cell",
    "SB01-029 Majin Buu : Evil"
    "SB01-045 Bulma",
    "FB07-001 Glorio : DA",
    "FB07-025 Syn Shenron",
    "FB07-049 Piccolo : SH",
    "FB07-073 Frieza",
    "FB07-097 Dragon Ball",
    "SB02-001 Trnks : Future",
    "SB02-017 Gotenks",
    "SB02-033 Son Goku",
    "FB08-001 Son Gohan : Adolescence",
    "FB08-025 Caulifla",
    "FB08-049 Turles",
    "FB08-073 Broly",
    "FB08-097 Son Goku Jr.",
    "FB09-001 Gogeta : BR", 
    "FB09-025 Son Goku",
    "FB09-049 Son Gohan : SH",
    "FB09-073 Son Goku/Vegeta",
    "FB09-097 Gogeta : GT",
    "FB10-001 Son Goku",
    "FB10-ß25 Son Goku/Vegeta",
    "FB10-049 Son Gohan : Youth/Piccolo",
    "FB10-073 Boujack",
    "FB10-097 Cell",
    "ST01-001 Son Goten",
    "ST01-027 Majin Buu/Majin Buu : Pure Evil",
    "ST01-053 Vegeta",
    "FB11-001 Son Goku",
    "FB11-025 Trunks : Future/Son Gohan : Future",
    "FB11-049 Goku Black",
    "FB11-073 Shallot/Giblet",
    "FB11-097 Bardock"
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

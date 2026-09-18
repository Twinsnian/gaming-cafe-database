# SJSU CMPE 138 FALL 2025 TEAM1
from application.utils.db import run_query, run_update, call_procedure
from application.utils.logger import log_info, log_error

def customer_menu(user):
    while True:
        print("\n=== Customer Menu ===")
        print("1. Browse Available Games")
        print("2. View My Game Sessions")
        print("3. Start a Game Session")
        print("4. End a Game Session")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            browse_games()
        elif choice == "2":
            view_sessions(user)
        elif choice == "3":
            start_session_ui(user)
        elif choice == "4":
            end_session_ui(user)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


def browse_games():
    print("\n--- Available Games ---")
    query = """
        SELECT GameID, Title, AgeRestriction, Platform, AvailabilityStatus
        FROM GameTitle
        WHERE AvailabilityStatus = 'Available'
        ORDER BY Title;
    """
    games = run_query(query)

    if not games:
        print("No games available.")
        return

    for g in games:
        print(f"[{g['GameID']}] {g['Title']} (Age {g['AgeRestriction']}+ | {g['Platform']})")


def view_sessions(user):
    print("\n--- Your Game Sessions ---")
    query = """
        SELECT gs.SessionID, gt.Title, gs.StartTime, gs.EndTime, gs.SessionStatus
        FROM GameSession gs
        JOIN GameTitle gt ON gs.GameID = gt.GameID
        WHERE gs.UserID = %s
        ORDER BY gs.StartTime DESC;
    """
    sessions = run_query(query, (user['id'],))

    if not sessions:
        print("You have no previous sessions.")
        return

    for s in sessions:
        print(f"Session {s['SessionID']}: {s['Title']} | {s['StartTime']} → {s['EndTime']} ({s['SessionStatus']})")


def start_session_ui(user):
    game_id = input("Enter Game ID: ")
    station_id = input("Enter Station ID: ")

    print("\nStarting session...")
    try:
        results = call_procedure("StartGameSession", (user['id'], int(game_id), int(station_id)))
        print("Session started:", results)
        log_info(f"User {user['id']} started session for game {game_id}")
    except Exception as e:
        print("Error starting session:", e)
        log_error(f"Start session failed: {e}")


def end_session_ui(user):
    session_id = input("Enter Session ID to end: ")

    print("\nEnding session...")
    try:
        # NOTE: EndGameSession expects OUT param — MySQL connector needs special handling.
        results = call_procedure("EndGameSession", (int(session_id),))
        print("Session ended:", results)
        log_info(f"User {user['id']} ended session {session_id}")
    except Exception as e:
        print("Error ending session:", e)
        log_error(f"End session failed: {e}")

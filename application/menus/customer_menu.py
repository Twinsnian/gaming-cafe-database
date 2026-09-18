# SJSU CMPE 138 FALL 2025 TEAM1
import os
import sys
import mysql.connector
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_NAME = os.getenv("DB_NAME", "gaming_cafe_db")

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=False
    )

def view_available_games(user_id: int):
    """Query 7: Available games for a specific user (age appropriate)."""
    sql = '''
SELECT 
    gt.GameID,
    gt.Title,
    gt.Genre,
    gt.Platform,
    gt.AgeRestriction,
    gt.MaxSessionTime,
    gt.AvailabilityStatus
FROM GameTitle gt
WHERE gt.AvailabilityStatus = 'Available'
  AND gt.AgeRestriction <= (
      SELECT TIMESTAMPDIFF(YEAR, DateOfBirth, CURDATE())
      FROM UserAccount
      WHERE UserID = %s
  )
ORDER BY gt.Title;
'''
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            print("\nAvailable Games:")
            print("GameID | Title | Genre | Platform | AgeRestr | MaxTime | Status")
            for r in rows:
                print(r)
    finally:
        conn.close()

def view_active_sessions_for_self(user_id: int):
    """Query 6 variant: show user's gaming history (active first)."""
    sql = '''
SELECT 
    gs.SessionID,
    gt.Title AS GamePlayed,
    s.Location AS StationLocation,
    gs.StartTime,
    gs.EndTime,
    gs.TotalTimePlayed AS MinutesPlayed,
    gs.SessionStatus
FROM GameSession gs
JOIN GameTitle gt ON gs.GameID = gt.GameID
JOIN Station s ON gs.StationID = s.StationID
WHERE gs.UserID = %s
ORDER BY gs.SessionStatus='Active' DESC, gs.StartTime DESC;
'''
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            print("\nYour Sessions (Active first):")
            print("(SessionID, Game, Station, Start, End, Minutes, Status)")
            for r in rows:
                print(r)
    finally:
        conn.close()

def view_promotions():
    """Query 10: Active promotions (date-range and IsActive=TRUE)."""
    sql = '''
SELECT 
    PromoID,
    PromoCode,
    Description,
    DiscountValue,
    StartDate,
    EndDate
FROM Promotions
WHERE IsActive = TRUE 
  AND CURDATE() BETWEEN StartDate AND EndDate
ORDER BY DiscountValue DESC;
'''
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print("\n   Active Promotions:")
            print("(PromoID, Code, Description, Discount, Start, End)")
            for r in rows:
                print(r)
    finally:
        conn.close()

def view_payment_history(user_id: int):
    """Query 8: User's payment history with promotions."""
    sql = '''
SELECT 
    p.InvoiceID,
    p.Amount,
    p.PaymentDateTime,
    p.PaymentMethod,
    pr.PromoCode,
    pr.Description AS PromoDescription,
    pr.DiscountValue
FROM Payment p
LEFT JOIN Promotions pr ON p.PromoApplied = pr.PromoID
WHERE p.UserID = %s
ORDER BY p.PaymentDateTime DESC;
'''
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            rows = cur.fetchall()
            print("\nYour Payments:")
            print("(InvoiceID, Amount, DateTime, Method, PromoCode, PromoDesc, Discount)")
            for r in rows:
                print(r)
    finally:
        conn.close()

def view_available_stations():
    """Query 9: Check available stations by type."""
    sql = '''
SELECT 
    StationID,
    StationType,
    Location,
    Status
FROM Station
WHERE Status = 'Available'
ORDER BY StationType, StationID;
'''
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print("\n️  Available Stations:")
            print("(StationID, Type, Location, Status)")
            for r in rows:
                print(r)
    finally:
        conn.close()

def start_session(user_id: int):
    """CALL StartGameSession(UserID, GameID, StationID)."""
    try:
        game_id = int(input("Enter GameID: "))
        station_id = int(input("Enter StationID: "))
    except ValueError:
        print("Invalid ids.")
        return
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.callproc("StartGameSession", [user_id, game_id, station_id])
            for result in cur.stored_results():
                rows = result.fetchall()
                if rows:
                    print("\n  StartGameSession result:")
                    for r in rows:
                        print(r)
        conn.commit()
        print(" Session started (if age and station checks passed).")
    except mysql.connector.Error as e:
        conn.rollback()
        print(" Failed to start session:", e)
    finally:
        conn.close()

def end_session():
    """CALL EndGameSession(SessionID, OUT AmountDue)."""
    try:
        session_id = int(input("Enter SessionID to end: "))
    except ValueError:
        print("Invalid session id.")
        return
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            args = [session_id, 0.0]
            result_args = cur.callproc("EndGameSession", args)
            for result in cur.stored_results():
                rows = result.fetchall()
                if rows:
                    print("\n️  EndGameSession result:")
                    for r in rows:
                        print(r)
            amount_due = result_args[1]
            print(f" Amount due (computed): ${amount_due:.2f}")
        conn.commit()
        print(" Session ended.")
    except mysql.connector.Error as e:
        conn.rollback()
        print(" Failed to end session:", e)
    finally:
        conn.close()

def prompt(msg: str) -> str:
    try:
        return input(msg)
    except EOFError:
        return ""

def main():
    if len(sys.argv) < 2:
        user_id = int(input("Enter your UserID: "))
    else:
        user_id = int(sys.argv[1])
    print(f" Welcome, User {user_id}!")
    while True:
        print("\n=== CUSTOMER MENU ===")
        print("1) View available games")
        print("2) View my sessions (active first)")
        print("3) Start session (CALL StartGameSession)")
        print("4) End session (CALL EndGameSession)")
        print("5) View promotions")
        print("6) View my payment history")
        print("7) View available stations")
        print("0) Exit")
        choice = prompt("> ")
        if choice == "1":
            view_available_games(user_id)
        elif choice == "2":
            view_active_sessions_for_self(user_id)
        elif choice == "3":
            start_session(user_id)
        elif choice == "4":
            end_session()
        elif choice == "5":
            view_promotions()
        elif choice == "6":
            view_payment_history(user_id)
        elif choice == "7":
            view_available_stations()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

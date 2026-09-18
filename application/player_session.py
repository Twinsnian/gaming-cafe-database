# SJSU CMPE 138 FALL 2025 TEAM1
import os
import mysql.connector

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

def start_session(user_id: int, game_id: int, station_id: int):
    """Wrap CALL StartGameSession(UserID, GameID, StationID)."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.callproc("StartGameSession", [user_id, game_id, station_id])
            for result in cur.stored_results():
                rows = result.fetchall()
                if rows:
                    return rows
        conn.commit()
        return [("Session started successfully", None)]
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def end_session(session_id: int):
    """Wrap CALL EndGameSession(SessionID, OUT AmountDue). Returns (amount_due, detailed_rows)."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            args = [session_id, 0.0]
            out_args = cur.callproc("EndGameSession", args)
            detailed_rows = []
            for result in cur.stored_results():
                detailed_rows.extend(result.fetchall())
        conn.commit()
        return out_args[1], detailed_rows
    except mysql.connector.Error:
        conn.rollback()
        raise
    finally:
        conn.close()

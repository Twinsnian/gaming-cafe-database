# SJSU CMPE 138 FALL 2025 TEAM1
# to connect to database

# utils/db.py
import mysql.connector
from mysql.connector import Error
from application.utils.config import DB_CONFIG
from application.utils.logger import log_info, log_error

def get_connection():
    """Establish a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        return conn
    except Error as e:
        log_error(f"Connection error: {e}")
        print(f"Database connection error: {e}")
        return None

def run_query(query, params=None):
    """Run a SELECT query and return results as a list of dictionaries."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        log_error(f"Query error: {e} | Query: {query}")
        print(f"Query error: {e}")
        return None

def run_update(query, params=None):
    """Run INSERT/UPDATE/DELETE queries."""
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        log_error(f"Update error: {e} | Query: {query}")
        print(f"Update error: {e}")
        return False

def call_procedure(proc_name, params=None):
    """Execute a stored procedure and return results (if any)."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, params)
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        conn.commit()
        cursor.close()
        conn.close()
        return results

    except Error as e:
        log_error(f"Procedure error: {e} | Procedure: {proc_name}")
        print(f"Procedure error: {e}")
        return None


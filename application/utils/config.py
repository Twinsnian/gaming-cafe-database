# SJSU CMPE 138 FALL 2025 TEAM1
# configurations for database (dp.py)

from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

#should input host name, user name, password, database name, and port# from the mysql server

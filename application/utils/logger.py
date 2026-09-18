# SJSU CMPE 138 FALL 2025 TEAM1
import logging
import os

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

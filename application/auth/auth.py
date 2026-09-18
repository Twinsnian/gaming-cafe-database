# SJSU CMPE 138 FALL 2025 TEAM1
import hashlib
from application.utils.db import run_query
from application.utils.logger import log_info, log_error

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    print("\n=== Login ===")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    hashed = hash_password(password)

    # Try customer
    user = run_query(
        "SELECT UserID AS id, FullName, PasswordHash, 'Customer' AS UserType "
        "FROM UserAccount WHERE Email = %s",
        (email,)
    )

    # Try staff
    staff = run_query(
        "SELECT EmployeeID AS id, FullName, Role AS UserType, PasswordHash "
        "FROM Employee WHERE Email = %s",
        (email,)
    )

    record = user[0] if user else (staff[0] if staff else None)

    if record is None:
        log_info(f"Login failed (not found): {email}")
        print("Invalid email or password.")
        return None

    if record["PasswordHash"] == hashed:
        log_info(f"Login success: {email}")
        return record
    else:
        log_info(f"Login failed (wrong password): {email}")
        print("Invalid email or password.")
        return None

# SJSU CMPE 138 FALL 2025 TEAM1
from application.utils.db import run_query, run_update, call_procedure
from application.auth.auth import hash_password
from application.utils.logger import log_info, log_error

def staff_menu(user):
    
    print(f"\n=== Staff Menu ===")
    print(f"Logged in as: {user['FullName']} ({user['UserType']})")

    role = user['UserType'].lower()

    if role == "administrator":
        admin_menu(user)
    elif role == "receptionist":
        receptionist_menu(user)
    elif role == "cashier":
        cashier_menu(user)
    elif role in ("gamemanager", "game manager", "game_manager"):
        game_manager_menu(user)
    elif role == "accountmanager":
        account_manager_menu(user)
    else:
        print("Unknown role")
        log_error(f"Unknown role for EmployeeID {user.get('EmployeeID')}")

# ADMIN FUNCTIONS
def admin_menu(user):
    while True:
        print("\n--- ADMIN MENU ---")
        print("1) View System Logs")
        print("2) Add/Edit Employee")
        print("3) Modify Station Status")
        print("4) View Analytics")
        print("5) Manage Promotions")
        print("6) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            view_system_logs()
        elif choice == "2":
            add_edit_employee()
        elif choice == "3":
            modify_station_status()
        elif choice == "4":
            view_analytics()
        elif choice == "5":
            manage_promotions()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

def view_system_logs():
    try:
        with open('application/logs/app.log', 'r') as f:
            print(f.read())
        log_info("Viewed system logs")
    except Exception as e:
        log_error(f"Failed to view logs: {e}")
        print("Error viewing logs")

def add_edit_employee():
    try:
        action = input("Add or Edit employee (A/E)? ").upper()
        name = input("Full Name: ")
        role = input("Role (Receptionist, Cashier, Administrator, GameManager): ")
        email = input("Email: ")
        pwd = input("Password: ")
        pwd_hash = hash_password(pwd)

        if action == "A":
            sql = "INSERT INTO Employee (FullName, Role, Email, PasswordHash) VALUES (%s,%s,%s,%s)"
            if run_update(sql, (name, role, email, pwd_hash)):
                log_info(f"Added employee: {name} ({role})")
                print("Employee added")
            else:
                print("Failed to add employee")
        elif action == "E":
            emp_id = int(input("EmployeeID to edit: "))
            sql = "UPDATE Employee SET FullName=%s, Role=%s, Email=%s, PasswordHash=%s WHERE EmployeeID=%s"
            if run_update(sql, (name, role, email, pwd_hash, emp_id)):
                log_info(f"Edited employee ID: {emp_id}")
                print("Employee updated")
            else:
                print("Failed to update employee")
        else:
            print("Invalid action")
    except Exception as e:
        log_error(f"Failed to add/edit employee: {e}")
        print("Error performing employee operation")

def modify_station_status():
    try:
        station_id = int(input("StationID: "))
        status = input("New Status (Available, Occupied, Maintenance): ")
        sql = "UPDATE Station SET Status=%s WHERE StationID=%s"
        if run_update(sql, (status, station_id)):
            log_info(f"Station {station_id} status updated to {status}")
            print("Station status updated")
        else:
            print("Failed to update station")
    except Exception as e:
        log_error(f"Failed to modify station status: {e}")
        print("Error modifying station")

def view_analytics():
    try:
        print("\n--- Revenue Report ---")
        rows = run_query("SELECT * FROM RevenueReport")
        if not rows:
            print("No revenue data available.")
        else:
            for r in rows:
                print(
                    f"Date: {r['PaymentDate']} | "
                    f"Transactions: {r['TotalTransactions']} | "
                    f"Revenue: ${r['TotalRevenue']} | "
                    f"Avg: ${r['AverageTransaction']} | "
                    f"Promo Uses: {r['TransactionsWithPromo']}"
                )

        print("\n--- Game Popularity ---")
        rows = run_query("SELECT * FROM GamePopularity")
        if not rows:
            print("No game popularity data available.")
        else:
            for r in rows:
                print(
                    f"{r['Title']} ({r['Genre']}) | "
                    f"Sessions: {r['TotalSessions']} | "
                    f"Minutes Played: {r['TotalMinutesPlayed']} | "
                    f"Avg Session: {r['AvgSessionLength']}"
                )

        log_info("Viewed analytics")

    except Exception as e:
        log_error(f"Failed to view analytics: {e}")
        print("Error viewing analytics")

def manage_promotions():
    while True:
        print("\n--- PROMOTION MANAGEMENT ---")
        print("1) Create Promotion")
        print("2) Update Promotion")
        print("3) End Promotion")
        print("4) Update Promotion Statuses")
        print("5) Back")

        choice = input("Select: ").strip()

        if choice == "1":
            create_promotion()
        elif choice == "2":
            update_promotion()
        elif choice == "3":
            end_promotion()
        elif choice == "4":
            update_promotion_statuses()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def create_promotion():
    try:
        promo_code = input("Promo Code: ").strip()
        description = input("Description: ")
        discount = float(input("Discount Value: "))
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")

        sql = """
            INSERT INTO Promotions (PromoCode, Description, DiscountValue, StartDate, EndDate, IsActive)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """

        if run_update(sql, (promo_code, description, discount, start_date, end_date)):
            print("Promotion created successfully!")
            log_info(f"Promotion created: {promo_code}")
        else:
            print("Failed to create promotion")
    except Exception as e:
        print("Error creating promotion:", e)
        log_error(f"Failed to create promo: {e}")

def update_promotion():
    try:
        promo_id = int(input("Promo ID to update: "))

        # Fetch promo first
        promo = run_query("SELECT * FROM Promotions WHERE PromoID=%s", (promo_id,))
        if not promo:
            print("Promotion not found.")
            return

        promo = promo[0]  # row

        print("\nLeave blank to keep current value.")
        new_code = input(f"Promo Code [{promo['PromoCode']}]: ") or promo['PromoCode']
        new_desc = input(f"Description [{promo['Description']}]: ") or promo['Description']
        new_discount = input(f"Discount Value [{promo['DiscountValue']}]: ")
        new_discount = float(new_discount) if new_discount else promo['DiscountValue']
        new_start = input(f"Start Date [{promo['StartDate']}]: ") or promo['StartDate']
        new_end = input(f"End Date [{promo['EndDate']}]: ") or promo['EndDate']

        sql = """
            UPDATE Promotions
            SET PromoCode=%s, Description=%s, DiscountValue=%s, 
                StartDate=%s, EndDate=%s
            WHERE PromoID=%s
        """

        if run_update(sql, (new_code, new_desc, new_discount, new_start, new_end, promo_id)):
            print("Promotion updated successfully!")
            log_info(f"Promotion updated: {promo_id}")
        else:
            print("Failed to update promotion")

    except Exception as e:
        print("Error updating promotion:", e)
        log_error(f"Failed to update promo: {e}")

def end_promotion():
    try:
        promo_id = int(input("Promo ID to end: "))
        yesterday = (datetime.today().date()).replace(day=datetime.today().day - 1)

        sql = """
            UPDATE Promotions
            SET IsActive = FALSE,
                EndDate = %s
            WHERE PromoID = %s
        """

        if run_update(sql, (yesterday, promo_id)):
            print(f"Promotion {promo_id} ended (EndDate set to {yesterday})")
            log_info(f"Promotion ended early: {promo_id}, set EndDate={yesterday}")
        else:
            print("Failed to end promotion")

    except Exception as e:
        print("Error ending promotion:", e)
        log_error(f"Failed to end promo: {e}")


def update_promotion_statuses():
    try:
        today = datetime.today().date()

        sql_expire = """
            UPDATE Promotions
            SET IsActive = FALSE
            WHERE EndDate < %s;
        """

        run_update(sql_expire, (today,))

        sql_activate = """
            UPDATE Promotions
            SET IsActive = TRUE
            WHERE StartDate <= %s AND EndDate >= %s;
        """

        run_update(sql_activate, (today, today))

        print("Promotion statuses updated based on current date.")
        log_info("Promotion statuses auto-updated")

    except Exception as e:
        print("Error updating promotion statuses:", e)
        log_error(f"Failed to update promotion statuses: {e}")

# RECEPTIONIST FUNCTIONS
def receptionist_menu(user):
    while True:
        print("\n--- RECEPTIONIST MENU ---")
        print("1) View Stations")
        print("2) Start Game Session")
        print("3) End Session")
        print("4) Pause/Resume Session")
        print("5) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            view_stations()
        elif choice == "2":
            start_game_session(user)
        elif choice == "3":
            end_game_session()
        elif choice == "4":
            update_session_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def view_stations():
    rows = run_query("SELECT * FROM Station ORDER BY StationID")
    for r in rows or []:
        print(r)
    log_info("Viewed stations")

def start_game_session(user):
    try:
        user_id = int(input("UserID: "))
        game_id = int(input("GameID: "))
        station_id = int(input("StationID: "))
        result = call_procedure("StartGameSession", [user_id, game_id, station_id])
        log_info(f"User {user_id} started session on Station {station_id} with Game {game_id}")
        print("Session started")
        if result:
            for r in result:
                print(r)
    except Exception as e:
        log_error(f"Failed to start game session: {e}")
        print("Error starting session")

def end_game_session():
    try:
        session_id = int(input("SessionID: "))
        result = call_procedure("EndGameSession", [session_id, 0.0])
        log_info(f"Ended session {session_id}")
        print("Session ended")
        if result:
            for r in result:
                print(r)
    except Exception as e:
        log_error(f"Failed to end game session: {e}")
        print("Error ending session")

def update_session_status():
    try:
        session_id = int(input("SessionID: "))
        status = input("New Status (Paused, Active, Finished, Cancelled): ")
        sql = "UPDATE GameSession SET SessionStatus=%s WHERE SessionID=%s"
        if run_update(sql, (status, session_id)):
            log_info(f"Updated session {session_id} status to {status}")
            print("Session status updated")
        else:
            print("Failed to update session status")
    except Exception as e:
        log_error(f"Failed to update session status: {e}")
        print("Error updating session status")

# CASHIER FUNCTIONS
def cashier_menu(user):
    while True:
        print("\n--- CASHIER MENU ---")
        print("1) Add Payment")
        print("2) List Active Promotions")
        print("3) Add User Credit")
        print("4) Apply Membership to User")
        print("5) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            add_payment(user)
        elif choice == "2":
            list_promotions()
        elif choice == "3":
            add_user_credit(user)
        elif choice == "4":
            apply_membership()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def add_payment(user):
    try:
        user_id = int(input("UserID: "))
        amount = float(input("Amount: "))
        method = input("Payment Method (Cash, Credit Card, Debit Card, Account Credit): ")
        promo = input("PromoID (or leave blank): ")
        promo_id = int(promo) if promo else None
        employee_id = user.get('EmployeeID')

        if promo_id:
            promo_row = run_query(
                "SELECT DiscountValue, StartDate, EndDate, IsActive "
                "FROM Promotions WHERE PromoID=%s", (promo_id,)
            )

            if not promo_row:
                print(" Invalid Promo ID - ignoring promo.")
                promo_id = None
            else:
                promo = promo_row[0]
                discount = float(promo["DiscountValue"])
                start = promo["StartDate"]
                end = promo["EndDate"]
                active = promo["IsActive"]

                today = datetime.today().date()

                if not active or today < start or today > end:
                    print("Promo is expired or inactive -  ignoring promo.")
                    promo_id = None
                else:
                    # APPLY DISCOUNT
                    discounted_amount = max(amount - discount, 0.0)
                    print(f"Promo applied! Discount: {discount:.2f}")
                    print(f"Original: {amount:.2f} | Final Amount: {discounted_amount:.2f}")
                    amount = discounted_amount

        # --- INSERT PAYMENT ---
        sql = """
            INSERT INTO Payment (UserID, EmployeeID, Amount, PaymentMethod, PromoApplied)
            VALUES (%s,%s,%s,%s,%s)
        """

        if run_update(sql, (user_id, employee_id, amount, method, promo_id)):
            print("Payment recorded")
            log_info(f"Payment added by Employee {employee_id} for User {user_id}, "
                     f"Amount: {amount}, Promo: {promo_id}")
        else:
            print("Failed to record payment")

    except Exception as e:
        log_error(f"Failed to add payment: {e}")
        print("Error adding payment")

def list_promotions():
    rows = run_query("SELECT * FROM Promotions WHERE IsActive=TRUE ORDER BY DiscountValue DESC")
    for r in rows or []:
        print(r)
    log_info("Viewed promotions")

def add_user_credit(user):
    try:
        user_id = int(input("UserID to credit: "))
        amount = float(input("Amount to add: "))
        employee_id = user['id']

        result = call_procedure("AddUserCredit", (user_id, amount, employee_id))

        log_info(f"Added {amount} credit to User {user_id} by Employee {employee_id}")
        print("Credit added successfully")

        for r in result or []:
            print(r)

    except Exception as e:
        print("Error adding user credit:", e)
        log_error(f"Failed to add user credit: {e}")

def apply_membership():
    try:
        user_id = int(input("Enter UserID to assign membership: "))

        user = run_query("SELECT * FROM UserAccount WHERE UserID=%s", (user_id,))
        if not user:
            print("User not found.")
            return

        print("\nMembership Types: Standard, Premium, VIP")
        m_type = input("Select membership type: ").strip().title()
        if m_type not in ("Standard", "Premium", "VIP"):
            print("Invalid membership type.")
            return

        start = datetime.today().date()
        end = start.replace(year=start.year + 1)

        sql = """
            INSERT INTO Membership (MembershipType, StartDate, EndDate, Status)
            VALUES (%s, %s, %s, 'Active')
        """
        run_update(sql, (m_type, start, end))

        membership_row = run_query(
            "SELECT MembershipID FROM Membership WHERE MembershipType=%s AND StartDate=%s ORDER BY MembershipID DESC LIMIT 1",
            (m_type, start)
        )
        if not membership_row:
            print("Failed to retrieve membership ID.")
            return

        mem_id = membership_row[0]['MembershipID']

        sql2 = "UPDATE UserAccount SET MembershipID=%s WHERE UserID=%s"
        if run_update(sql2, (mem_id, user_id)):
            print(f"Assigned {m_type} membership (ID {mem_id}) to User {user_id}")
            log_info(f"Assigned membership {mem_id} ({m_type}) to user {user_id}")
        else:
            print("Failed to link membership to user.")

    except Exception as e:
        print("Error applying membership:", e)
        log_error(f"Failed to apply membership: {e}")

# GAME MANAGER FUNCTIONS
def game_manager_menu(user):
    while True:
        print("\n--- GAME MANAGER MENU ---")
        print("1) List Games")
        print("2) Add Game")
        print("3) Update Game")
        print("4) Remove Game")
        print("5) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            list_games()
        elif choice == "2":
            add_game()
        elif choice == "3":
            update_game()
        elif choice == "4":
            remove_game()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def list_games():
    rows = run_query("SELECT * FROM GameTitle ORDER BY Title")
    for r in rows or []:
        print(r)
    log_info("Viewed game list")

def add_game():
    try:
        title = input("Game Title: ")
        genre = input("Genre: ")
        age = int(input("Age Restriction: "))
        max_time = int(input("Max Session Time: "))
        platform = input("Platform (PC, Console, Both): ")
        sql = "INSERT INTO GameTitle (Title, Genre, AgeRestriction, MaxSessionTime, Platform) VALUES (%s,%s,%s,%s,%s)"
        if run_update(sql, (title, genre, age, max_time, platform)):
            log_info(f"Added game: {title}")
            print("Game added")
        else:
            print("Failed to add game")
    except Exception as e:
        log_error(f"Failed to add game: {e}")
        print("Error adding game")

def update_game():
    try:
        game_id = int(input("GameID to update: "))
        title = input("New Title: ")
        genre = input("Genre: ")
        age = int(input("Age Restriction: "))
        max_time = int(input("Max Session Time: "))
        platform = input("Platform: ")
        status = input("AvailabilityStatus (Available, Maintenance, Unavailable): ")
        sql = """
        UPDATE GameTitle
        SET Title=%s, Genre=%s, AgeRestriction=%s, MaxSessionTime=%s, Platform=%s, AvailabilityStatus=%s
        WHERE GameID=%s
        """
        if run_update(sql, (title, genre, age, max_time, platform, status, game_id)):
            log_info(f"Updated game {game_id}: {title}")
            print("Game updated")
        else:
            print("Failed to update game")
    except Exception as e:
        log_error(f"Failed to update game: {e}")
        print("Error updating game")

def remove_game():
    try:
        game_id = int(input("GameID to remove: "))
        sql = "DELETE FROM GameTitle WHERE GameID=%s"
        if run_update(sql, (game_id,)):
            log_info(f"Removed game {game_id}")
            print("Game removed")
        else:
            print("Failed to remove game")
    except Exception as e:
        log_error(f"Failed to remove game: {e}")
        print("Error removing game")

# ACCOUNT MANAGER
def account_manager_menu(user):
    while True:
        print("\n--- ACCOUNT MANAGER MENU ---")
        print("1) Create User Account")
        print("2) Edit User Account")
        print("3) Deactivate User Account")
        print("4) Merge User Accounts")
        print("5) Recover User Account")
        print("6) Set/Update Guardian for Minor")
        print("7) Change User Password")
        print("8) Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            create_user_account()
        elif choice == "2":
            edit_user_account()
        elif choice == "3":
            deactivate_user_account()
        elif choice == "4":
            merge_user_accounts()
        elif choice == "5":
            recover_user_account()
        elif choice == "6":
            update_guardian()
        elif choice == "7":
            change_user_password()
        elif choice == "8":
            break
        else:
            print("Invalid choice")

from datetime import datetime
from application.utils.db import run_update
from application.auth.auth import hash_password
from application.utils.logger import log_info, log_error

def create_user_account():
    try:
        full_name = input("Full Name: ")
        dob_str = input("Date of Birth (YYYY-MM-DD): ")
        email = input("Email: ")
        phone = input("Phone: ")
        pwd = input("Password: ")
        pwd_hash = hash_password(pwd)

        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        today = datetime.today().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        is_minor = 1 if age < 18 else 0

        sql = """
        INSERT INTO UserAccount
        (FullName, DateOfBirth, Email, Phone, PasswordHash, IsMinor)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        result = run_update(sql, (full_name, dob, email, phone, pwd_hash, is_minor))

        if result is False or result is None:
            print("Error creating user account")
            return

        print("User account created successfully")
        log_info(f"Created user account for {full_name}")

    except Exception as e:
        print("Error creating user account:", e)
        log_error(f"Failed to create user account: {e}")

def edit_user_account():
    try:
        user_id = int(input("UserID to edit: "))
        print("Enter new values (leave blank to keep current value)")
        user = run_query("SELECT * FROM UserAccount WHERE UserID=%s", (user_id,))
        if not user:
            print("User not found")
            return
        user = user[0]

        full_name = input(f"Full Name ({user['FullName']}): ") or user['FullName']
        dob = input(f"Date of Birth ({user['DateOfBirth']}): ") or user['DateOfBirth']
        email = input(f"Email ({user['Email']}): ") or user['Email']
        phone = input(f"Phone ({user['Phone']}): ") or user['Phone']

        sql = """
        UPDATE UserAccount
        SET FullName=%s, DateOfBirth=%s, Email=%s, Phone=%s
        WHERE UserID=%s
        """
        run_update(sql, (full_name, dob, email, phone, user_id))
        log_info(f"Edited user account {user_id}")
        print("User account updated successfully")
    except Exception as e:
        log_error(f"Failed to edit user account: {e}")
        print("Error editing user account")

def deactivate_user_account():
    try:
        user_id = int(input("UserID to deactivate: "))
        sql = "UPDATE UserAccount SET AccountStatus='Suspended' WHERE UserID=%s"
        run_update(sql, (user_id,))
        log_info(f"Deactivated user account {user_id}")
        print("User account deactivated")
    except Exception as e:
        log_error(f"Failed to deactivate account: {e}")
        print("Error deactivating account")

def recover_user_account():
    try:
        user_id = int(input("UserID to recover: "))
        sql = "UPDATE UserAccount SET AccountStatus='Active' WHERE UserID=%s"
        run_update(sql, (user_id,))
        log_info(f"Recovered user account {user_id}")
        print("User account recovered successfully")
    except Exception as e:
        log_error(f"Failed to recover account: {e}")
        print("Error recovering account")

def merge_user_accounts():
    try:
        source_id = int(input("Source UserID (to merge from): "))
        target_id = int(input("Target UserID (to merge into): "))

        # Move payments
        sql_payments = "UPDATE Payment SET UserID=%s WHERE UserID=%s"
        run_update(sql_payments, (target_id, source_id))

        # Move sessions
        sql_sessions = "UPDATE GameSession SET UserID=%s WHERE UserID=%s"
        run_update(sql_sessions, (target_id, source_id))

        sql_delete = "DELETE FROM UserAccount WHERE UserID=%s"
        run_update(sql_delete, (source_id,))

        log_info(f"Merged user account {source_id} into {target_id}")
        print(f"User accounts merged: {source_id} → {target_id}")
    except Exception as e:
        log_error(f"Failed to merge accounts: {e}")
        print("Error merging accounts")

def update_guardian():
    try:
        minor_id = int(input("Minor UserID: "))
        guardian_id = int(input("Guardian UserID: "))
        sql = "UPDATE UserAccount SET GuardianID=%s WHERE UserID=%s"
        run_update(sql, (guardian_id, minor_id))
        log_info(f"Set guardian {guardian_id} for minor {minor_id}")
        print("Guardian updated successfully")
    except Exception as e:
        log_error(f"Failed to update guardian: {e}")
        print("Error updating guardian")

def change_user_password():
    try:
        user_id = int(input("UserID to change password: "))
        new_password = input("New password: ")
        pwd_hash = hash_password(new_password)

        sql = "UPDATE UserAccount SET PasswordHash = %s WHERE UserID = %s"
        result = run_update(sql, (pwd_hash, user_id))

        if not result:  
            print("No user found with that ID.")
            return

        print("Password updated successfully.")
        log_info(f"Password updated for UserID {user_id}")

    except Exception as e:
        print("Error updating password:", e)
        log_error(f"Failed to update password for User {user_id}: {e}")

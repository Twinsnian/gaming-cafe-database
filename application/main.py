# SJSU CMPE 138 FALL 2025 TEAM1
from application.auth.auth import login
from application.menus.customer_menu import main as customer_menu
from application.menus.staff_menu import staff_menu

def main():
    print("======================================")
    print("      Gaming Cafe CLI Application     ")
    print("======================================")

    user = None
    while user is None:
        user = login()

    print(f"\nWelcome, {user['FullName']} ({user['UserType']})")

    if user["UserType"] == "Customer":
        customer_menu()
    else:
        staff_menu(user)

if __name__ == "__main__":
    main()

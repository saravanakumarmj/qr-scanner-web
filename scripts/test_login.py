"""Temporary manual test for application login."""

from getpass import getpass

from services.auth_service import login


def main() -> None:
    user_id = input("User ID: ").strip()
    password = getpass("Password: ")

    try:
        user = login(user_id, password)

        print()
        print("Login successful")
        print(f"User ID:  {user.user_id}")
        print(f"Name:     {user.full_name}")
        print(f"Role:     {user.role}")
        print(f"Auth ID:  {user.auth_user_id}")

    except Exception as exc:
        print()
        print(f"Login failed: {exc}")


if __name__ == "__main__":
    main()
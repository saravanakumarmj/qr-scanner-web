"""One-time utility for creating the initial QR Management administrator."""

from getpass import getpass

from services.user_service import create_user


def main() -> None:
    print("QR Management System - Initial Administrator")
    print("-" * 45)

    user_id = input("Admin User ID: ").strip()
    full_name = input("Admin Name: ").strip()

    password = getpass("Admin Password: ")
    confirm_password = getpass("Confirm Password: ")

    if password != confirm_password:
        raise SystemExit("Passwords do not match.")

    if len(password) < 5:
        raise SystemExit("Password must be at least 5 characters.")

    try:
        user = create_user(
            user_id=user_id,
            password=password,
            full_name=full_name,
            role="ADMIN",
        )

        print()
        print("Administrator created successfully.")
        print(f"User ID: {user['user_id']}")
        print(f"Name:    {user['full_name']}")
        print(f"Role:    {user['role']}")

    except Exception as exc:
        raise SystemExit(f"Failed to create administrator: {exc}")


if __name__ == "__main__":
    main()
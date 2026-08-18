import getpass
from datetime import datetime

from src.database import SessionLocal
from src.crud import create_user, get_user_by_username, get_user_by_email


def main():
    username = input("Username [admin]: ").strip() or "admin"
    full_name = input("Họ tên [Quản trị hệ thống CENCOM]: ").strip() or "Quản trị hệ thống CENCOM"
    email = input("Email: ").strip()

    if not email:
        print("LỖI: Email không được để trống.")
        return

    password = getpass.getpass("Mật khẩu: ")
    password_confirm = getpass.getpass("Nhập lại mật khẩu: ")

    if password != password_confirm:
        print("LỖI: Hai mật khẩu không giống nhau.")
        return

    if len(password) < 8:
        print("LỖI: Mật khẩu phải có ít nhất 8 ký tự.")
        return

    db = SessionLocal()

    try:
        if get_user_by_username(db, username):
            print(f"LỖI: Username '{username}' đã tồn tại.")
            return

        if get_user_by_email(db, email):
            print(f"LỖI: Email '{email}' đã tồn tại.")
            return

        user = create_user(
            db=db,
            username=username,
            full_name=full_name,
            email=email,
            password=password,
        )

        print()
        print("========================================")
        print("TẠO TÀI KHOẢN ADMIN THÀNH CÔNG")
        print("========================================")
        print(f"ID       : {user.id}")
        print(f"Username : {user.username}")
        print(f"Họ tên   : {user.full_name}")
        print(f"Email    : {user.email}")
        print(f"Active   : {user.is_active}")
        print("========================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
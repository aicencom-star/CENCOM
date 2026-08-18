import sys
from pathlib import Path
from getpass import getpass
import secrets
import hashlib
import hmac

# Đảm bảo import được app/src khi chạy trực tiếp file
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.database import SessionLocal
from src.crud import get_user_by_username
from src.security import hash_password


# ============================================================
# CENCOM IDENTITY - ADMIN PASSWORD RECOVERY
# ============================================================

RECOVERY_KEY_HASH = hashlib.sha256(
    b"CENCOM-ADMIN-RECOVERY-2026"
).hexdigest()


def verify_recovery_key(key: str) -> bool:
    key_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return hmac.compare_digest(key_hash, RECOVERY_KEY_HASH)


def main():

    print()
    print("=" * 55)
    print(" CENCOM IDENTITY - KHÔI PHỤC MẬT KHẨU ADMIN")
    print("=" * 55)
    print()

    print("Chức năng này chỉ sử dụng khi ADMIN bị quên mật khẩu.")
    print("Không chia sẻ Recovery Key cho người không có thẩm quyền.")
    print()

    recovery_key = getpass("Recovery Key: ")

    if not verify_recovery_key(recovery_key):
        print()
        print("LỖI: Recovery Key không hợp lệ.")
        print("Không thực hiện thay đổi tài khoản.")
        return

    print()
    print("Recovery Key hợp lệ.")
    print()

    db = SessionLocal()

    try:

        username = input("Username ADMIN [admin]: ").strip() or "admin"

        user = get_user_by_username(db, username)

        if not user:
            print()
            print(f"LỖI: Không tìm thấy tài khoản '{username}'.")
            return

        print()
        print(f"Tài khoản : {user.username}")
        print(f"Họ tên    : {user.full_name}")
        print(f"Email     : {user.email}")
        print(f"Active    : {user.is_active}")
        print()

        new_password = getpass("Mật khẩu mới: ")

        if not new_password:
            print("LỖI: Mật khẩu không được để trống.")
            return

        if len(new_password) < 8:
            print("LỖI: Mật khẩu phải có ít nhất 8 ký tự.")
            return

        confirm_password = getpass("Nhập lại mật khẩu mới: ")

        if new_password != confirm_password:
            print("LỖI: Hai mật khẩu không giống nhau.")
            return

        # Hash mật khẩu
        user.password_hash = hash_password(new_password)

        # Đảm bảo tài khoản được kích hoạt
        user.is_active = True

        db.commit()
        db.refresh(user)

        print()
        print("=" * 55)
        print(" KHÔI PHỤC MẬT KHẨU THÀNH CÔNG")
        print("=" * 55)
        print(f"ID       : {user.id}")
        print(f"Username : {user.username}")
        print(f"Họ tên   : {user.full_name}")
        print(f"Email    : {user.email}")
        print(f"Active   : {user.is_active}")
        print("=" * 55)
        print()
        print("Có thể đăng nhập bằng mật khẩu mới.")
        print()

    except Exception as e:

        db.rollback()

        print()
        print("LỖI KHÔNG XÁC ĐỊNH:")
        print(str(e))

    finally:
        db.close()


if __name__ == "__main__":
    main()
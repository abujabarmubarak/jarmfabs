import sys
import getpass
from app import app
from models import db, AdminUser

def change_credentials(username=None, password=None):
    with app.app_context():
        if not username:
            username = input("Enter new admin username (e.g. admin or your name): ").strip()
        if not password:
            password = getpass.getpass("Enter new admin password: ").strip()
            confirm = getpass.getpass("Confirm new admin password: ").strip()
            if password != confirm:
                print("Error: Passwords do not match.")
                sys.exit(1)

        if not username or not password:
            print("Error: Username and password cannot be empty.")
            sys.exit(1)

        admin = AdminUser.query.first()
        if admin:
            admin.username = username
            admin.set_password(password)
            db.session.commit()
            print(f"[OK] Admin credentials updated successfully in database! Username: '{username}'")
        else:
            admin = AdminUser(username=username)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print(f"[OK] New admin user created! Username: '{username}'")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        change_credentials(sys.argv[1], sys.argv[2])
    else:
        print("--- JarmFabs Admin Credential Manager ---")
        change_credentials()

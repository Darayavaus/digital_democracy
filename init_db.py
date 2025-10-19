# init_db.py
from db import init_metadata

def init_db():
    init_metadata()
    print("✅ Database initialized (tables created if missing).")

if __name__ == "__main__":
    init_db()


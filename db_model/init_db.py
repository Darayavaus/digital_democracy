from db_model.db import init_metadata

# init_db.py
def init_db():
    init_metadata()
    print("✅ Database initialized (tables created if missing).")

if __name__ == "__main__":
    init_db()


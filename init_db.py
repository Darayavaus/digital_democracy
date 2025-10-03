# init_db.py
print("Step 1: Connecting...")

from sqlmodel import SQLModel
from db import engine

# Import all models so SQLModel knows about them
from models import participant, process, proposal, vote  # noqa: F401

def init_db():
    print("Step 2: Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    init_db()

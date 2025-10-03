from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///luxdemocracy.db"

# echo=True prints the generated SQL (helpful while learning/debugging)
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    """Helper to open a new DB session"""
    return Session(engine)

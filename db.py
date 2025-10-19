from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///luxdemocracy.db", echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_metadata() -> None:
    from models import (
        attachment,
        initiative,
        initiative_thematic,
        institution,
        milestone,
        polis,
        politician,
        thematic,
    )
    SQLModel.metadata.create_all(engine)

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

# Database setup
database_url = "sqlite:///luxdemocracy.db"
engine = create_engine(database_url, echo=False)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency 
def get_session():
    with Session(engine) as session:
        yield session

# Execute CREATE TABLE statements for any tables in metadata
# that don't already exist in the database 
def init_metadata() -> None:
    SQLModel.metadata.create_all(engine)

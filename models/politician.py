from sqlmodel import SQLModel, Field

class Politician(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    ministry: str
    party: str

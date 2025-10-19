from sqlmodel import SQLModel, Field

class Institution(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    institution: str
    party: str
from typing import Optional
from sqlmodel import SQLModel, Field


class Politician(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ministry: str
    party: str

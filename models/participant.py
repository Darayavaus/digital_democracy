from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str
    email: str

    proposals: List["Proposal"] = Relationship(back_populates="author")
    votes: List["Vote"] = Relationship(back_populates="voter")

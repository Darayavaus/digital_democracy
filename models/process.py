from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Process(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str = "open"

    proposals: List["Proposal"] = Relationship(back_populates="process")

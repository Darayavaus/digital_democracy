from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Proposal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    process_id: int = Field(foreign_key="process.id")
    author_id: int = Field(foreign_key="participant.id")
    title: str
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    process: "Process" = Relationship(back_populates="proposals")
    author: "Participant" = Relationship(back_populates="proposals")
    votes: List["Vote"] = Relationship(back_populates="proposal")

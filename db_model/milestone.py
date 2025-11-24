from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, timezone


if TYPE_CHECKING:
    from db_model.commitment import Commitment

class Milestone(SQLModel, table=True):
    """
    TODO: Add docstring
    """
    __tablename__ ='milestone'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    summary: str
    body: str
    due_date: datetime | None = None
    completion_date: datetime | None = None
    budget: int
    notes: str
    
    commitment_id: Optional[int] = Field(default=None, foreign_key="commitment.id")
    commitment: Optional['Commitment'] = Relationship(back_populates="milestones")

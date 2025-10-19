from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Milestone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    summary: str
    body: str
    due_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    budget: int
    notes: str
    
    initiative_id: int = Field(foreign_key="initiative.id")
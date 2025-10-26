from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db_model.commitment import Commitment
    from db_model.resources import Resources

class Context(SQLModel, table=True):
    __tablename__ = "context"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    subtitle: str | None = None
    body: str | None = None

    commitment_id: int = Field(foreign_key="commitment.id")
    commitment: 'Commitment' = Relationship(back_populates="context")
    relevant_studies: list['Resources'] = Relationship(back_populates="context")




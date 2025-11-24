from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db_model.commitment import Commitment
    from db_model.resources import Resources

class Context(SQLModel, table=True):
    """
    TODO: Add description
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    subtitle: str | None = None
    body: str | None = None

    commitment_id: Optional[int] = Field(default=None, foreign_key="commitment.id")
    commitment: Optional['Commitment'] = Relationship(back_populates="context")
    resources: list['Resources'] = Relationship(back_populates="context")




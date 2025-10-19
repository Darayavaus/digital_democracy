from __future__ import annotations
from datetime import date
from typing import Any
from sqlmodel import SQLModel, Field, Relationship
from .initiative_thematic import InitiativeThematic

class Initiative(SQLModel, table=True):
    __tablename__ = "initiative"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    summary: str | None = None
    body: str | None = None
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    budget: int | None = None
    owner_id: int | None = Field(default=None, foreign_key="institution.id")

    # ✅ Add annotation to satisfy SQLModel
    thematics: Any = Relationship(
        back_populates="initiatives",
        link_model=InitiativeThematic,
    )

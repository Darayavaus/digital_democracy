from __future__ import annotations
from typing import Any
from sqlmodel import SQLModel, Field, Relationship

class Polis(SQLModel, table=True):
    __tablename__ = "polis"

    id: int | None = Field(default=None, primary_key=True)
    summary: str | None = None
    polis_url: str
    thematic_id: int = Field(foreign_key="thematics.id")

    thematic: Any = Relationship(back_populates="polis_threads")

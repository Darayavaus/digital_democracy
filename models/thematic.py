from __future__ import annotations
from typing import Any
from sqlmodel import SQLModel, Field, Relationship
from .initiative_thematic import InitiativeThematic

class Thematic(SQLModel, table=True):
    __tablename__ = "thematics"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(index=True, unique=True)
    description: str | None = None

    initiatives: Any = Relationship(
        back_populates="thematics",
        link_model=InitiativeThematic,
    )

    polis_threads: Any = Relationship(back_populates="thematic")

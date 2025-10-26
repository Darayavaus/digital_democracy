from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from domain_model.ministry import Ministry

if TYPE_CHECKING:
    from db_model.context import Context
    from db_model.kpi import KPI
    from db_model.milestone import Milestone

class Commitment(SQLModel, table=True):
    __tablename__ = "commitment"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    ministry: Ministry
    summary: str | None = None
    body: str | None = None
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    budget: int | None = None

    milestones: list['Milestone'] = Relationship(back_populates="commitment")
    kpis: list['KPI'] = Relationship(back_populates="commitment")
    context: list['Context'] = Relationship(back_populates="commitment")




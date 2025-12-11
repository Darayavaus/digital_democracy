from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship

from db_model.law_commitment_link import DraftLawCommitmentLink
from domain_model.ministry import Ministry

if TYPE_CHECKING:
    from db_model.context import Context
    from db_model.draft_law import DraftLaw
    from db_model.kpi import KPI
    from db_model.milestone import Milestone

class Commitment(SQLModel, table=True):
    """
    TODO: Add description
    """
    __tablename__ = "commitment"
    id: Optional[int] = Field(default=None, primary_key=True)
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
    ##draft_laws: list["DraftLaw"] = Relationship(back_populates="commitments", link_model=DraftLawCommitmentLink)
    draft_laws: List["DraftLaw"] = Relationship(back_populates="commitments", link_model=DraftLawCommitmentLink)
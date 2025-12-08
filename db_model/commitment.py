from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

from db_model.draft_law import DraftLaw
from db_model.law_commitment_link import DraftLawCommitmentLink
from domain_model.ministry import Ministry

if TYPE_CHECKING:
    from db_model.context import Context
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
    draft_laws: list["DraftLaw"] = Relationship(back_populates="commitments", link_model=DraftLawCommitmentLink)



my_commitment_1 = Commitment(
    title="Commitment 1",
    ministry=Ministry.ECONOMIE,
    summary="Summary 1",
    body="Body 1",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    budget=100000,
)

my_commitment_2 = Commitment(
    title="Commitment 1",
    ministry=Ministry.ECONOMIE,
    summary="Summary 1",
    body="Body 1",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    budget=100000,
)

my_draft_law = DraftLaw(
    law_number=1,
    law_type=LawType.GOVT_DRAFT_LAW,
    law_deposit_date=date(2024, 1, 1),
    law_evacuation_date=date(2024, 12, 31),
    law_status=LawStatus.CREATED,
    law_title="Law Title 1",
    law_content="Law Content 1",
    law_authors="Law Authors 1",
    commitments=[my_commitment_1, my_commitment_2, ],
)




session.add(my_draft_law)
session.commit()




draft_law_in_db = session.query(DraftLaw).filter(DraftLaw.law_number == 1).first()

draft_law_in_db.commitments.append(new_commitment)
session.commit()
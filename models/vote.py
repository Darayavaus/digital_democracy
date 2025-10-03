from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

class Vote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposal_id: int = Field(foreign_key="proposal.id")
    voter_id: int = Field(foreign_key="participant.id")
    value: int = 1

    proposal: "Proposal" = Relationship(back_populates="votes")
    voter: "Participant" = Relationship(back_populates="votes")

    __table_args__ = (
        UniqueConstraint("proposal_id", "voter_id", name="uq_vote_once"),
    )

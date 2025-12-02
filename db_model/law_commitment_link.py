from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class DraftLawCommitmentLink(SQLModel, table=True):
    __tablename__ = "draft_law_commitment_link"
    draft_law_id: int = Field(foreign_key="draft_law.id", primary_key=True)
    commitment_id: int = Field(foreign_key="commitment.id", primary_key=True) 


from typing import Optional
from sqlmodel import SQLModel, Field


class DraftLawCommitmentLink(SQLModel, table=True):
    __tablename__ = "draft_law_commitment_link"
    draft_law_id: int = Field(primary_key= True, foreign_key="draft_law.id")
    commitment_id: int = Field(primary_key= True, foreign_key="commitment.id") 


from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class DraftLawCommitmentLink(SQLModel, table=True):
    __tablename__ = "draft_law_commitment_link"
    id: Optional[int] = Field(default=None, primary_key=True)
    draft_law_id: int = Field(foreign_key="draft_law.id")
    commitment_id: int = Field(foreign_key="commitment.id") 


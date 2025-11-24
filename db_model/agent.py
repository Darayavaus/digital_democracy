from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from db_model.commitment import Commitment
from domain_model.governance import Governance

class Agent(SQLModel, table=True):
    """
    TODO: Add description
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    gov_level: Governance
    commitments: list[Commitment] = Relationship(back_populates="agents")

from sqlmodel import Relationship, SQLModel, Field

from db_model.commitment import Commitment
from domain_model.governance import Governance

class Agent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    gov_level: Governance
    commitments: list[Commitment] = Relationship(back_populates="agents")

from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from db_model.commitment import Commitment
from domain_model.kpi_type import KpiType

class KPI(SQLModel, table=True):
    """
    TODO: Add description
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    type: KpiType
    value: float
    unit: str
    
    commitment_id: Optional[int] = Field(default=None, foreign_key="commitment.id")
    commitment: Optional['Commitment'] = Relationship(back_populates="kpis")

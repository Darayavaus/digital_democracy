from sqlmodel import SQLModel, Field

from domain_model.kpi_type import KpiType

class KPI(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: KpiType
    value: int | float
    unit: str
    
    commitment_id: int = Field(foreign_key="commitment.id")

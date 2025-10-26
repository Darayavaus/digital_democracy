from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field


from sqlmodel import Relationship

if TYPE_CHECKING:
    from db_model.context import Context

class Resources(SQLModel, table=True):
    __tablename__ = "resources"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    url: str
    
    context_id: int = Field(foreign_key="context.id")
    context: 'Context' = Relationship(back_populates="resources")
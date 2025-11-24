from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field


from sqlmodel import Relationship

if TYPE_CHECKING:
    from db_model.context import Context

class Resources(SQLModel, table=True):
    """
    TODO: Add docstring
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
    
    context_id: Optional[int] = Field(default=None, foreign_key="context.id")
    context: Optional['Context'] = Relationship(back_populates="resources")

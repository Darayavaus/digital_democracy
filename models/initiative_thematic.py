from sqlmodel import SQLModel, Field

class InitiativeThematic(SQLModel, table=True):
    __tablename__ = "initiative_thematic"
    initiative_id: int = Field(foreign_key="initiative.id", primary_key=True)
    thematic_id: int = Field(foreign_key="thematics.id", primary_key=True)

from sqlmodel import SQLModel, Field

class Attachment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    file_url: str | None = None
    
    initiative_id: int = Field(foreign_key="initiative.id")
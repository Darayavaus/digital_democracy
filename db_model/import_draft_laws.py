import pandas as pd
import datetime
from sqlmodel import Session
from db_model.db import engine, init_metadata

# Importing necessary models
from db_model.draft_law import INPUT_LAW_STATUS_MAPPING, DraftLaw, LawStatus

## Import excel file 
def import_draft_laws(): 
    
    # Create database tables if they do not already exist in luxdemocracy.db
    init_metadata() 

    with Session(engine) as session:
        df = pd.read_excel('static/112-texte-loi.xlsx')
        #create SQLModel instances for each row and add to session
        for index, row in df.iterrows():
            draft_law = DraftLaw(
                law_number=row['law_number'],
                law_type=row['law_type'],
                law_deposit_date=convertdate(str(row['law_deposit_date'])),
                law_evacuation_date=convertdate(str(row['law_evacuation_date'])),
                law_status=INPUT_LAW_STATUS_MAPPING.get(row['law_status'], LawStatus.Vide),
                law_title=row['law_title'],
                law_content=row['law_content'],
                law_authors=row['law_authors']
            )
            session.add(draft_law)
            session.commit()
        print(f"✅ Imported {len(df)} rows successfully")

def convertdate(date_str: str) -> datetime.date:
    """Convert a date string in 'dd/mm/yyyy' format to a datetime.date object."""
    if date_str == "nan": 
        return None
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

if __name__ == "__main__":
    import_draft_laws()
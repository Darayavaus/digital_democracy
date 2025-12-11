import pandas as pd
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
        for index, row in df.itertuples():
            draft_law = DraftLaw(
                law_number=row['law_number'],
                law_type=row['law_type'],
                law_deposit_date=row['law_deposit_date'],
                law_evacuation_date=row['law_evacuation_date'],
                law_status=INPUT_LAW_STATUS_MAPPING.get(row['law_status'], LawStatus.Vide),
                law_title=row['law_title'],
                law_content=row['law_content'],
                law_authors=row['law_authors']
            )
            session.add(draft_law)
        session.commit()

if __name__ == "__main__":
    import_draft_laws()
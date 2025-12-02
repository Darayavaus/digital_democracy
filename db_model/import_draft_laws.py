import pandas as pd
from sqlalchemy.orm import Session
from db_model.db import engine

from db_model.draft_law import INPUT_LAW_STATUS_MAPPING, DraftLaw, LawStatus


## Import excel file 


def import_draft_laws(): 
    with Session(engine) as session:
        df = pd.read_excel('static/112-texte-loi.xlsx')
        for index, row in df.iterrows():
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

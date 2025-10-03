from fastapi import FastAPI, Depends
from sqlmodel import select
from db import get_session
from models.participant import Participant
from models.process import Process
from models.proposal import Proposal
from models.vote import Vote
from models.politician import Politician
from typing import Optional

app = FastAPI(title="Digital Democracy API")

# Dependency injection for DB session
def get_db():
    with get_session() as session:
        yield session


@app.get("/")
def read_root():
    return {"message": "Welcome to Digital Democracy"}


@app.get("/participants")
def list_participants(session=Depends(get_db)):
    return session.exec(select(Participant)).all()


@app.get("/processes")
def list_processes(session=Depends(get_db)):
    return session.exec(select(Process)).all()


@app.get("/proposals/{process_id}")
def proposals_for_process(process_id: int, session=Depends(get_db)):
    statement = select(Proposal).where(Proposal.process_id == process_id)
    return session.exec(statement).all()


@app.get("/votes/{proposal_id}")
def votes_for_proposal(proposal_id: int, session=Depends(get_db)):
    statement = select(Vote).where(Vote.proposal_id == proposal_id)
    return session.exec(statement).all()

@app.get("/politicians")
def list_politicians(
    party: Optional[str] = None,
    session=Depends(get_db)
):
    stmt = select(Politician)
    if party:
        stmt = stmt.where(Politician.party == party)
    return session.exec(stmt).all()


@app.get("/politicians/{politician_id}")
def get_politician(politician_id: int, session=Depends(get_db)):
    pol = session.get(Politician, politician_id)
    if not pol:
        return {"detail": "Politician not found"}
    return pol


@app.post("/politicians", status_code=201)
def create_politician(politician: Politician, session=Depends(get_db)):
    session.add(politician)
    session.commit()
    session.refresh(politician)
    return politician


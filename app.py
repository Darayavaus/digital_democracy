from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlmodel import Session, select

from db import get_session, init_metadata
from models.attachment import Attachment
from models.initiative import Initiative
from models.institution import Institution
from models.milestone import Milestone
from models.polis import Polis
from models.thematic import Thematic

# --------------------------------------------------------------------
# App & Jinja setup
# --------------------------------------------------------------------
BASE_DIR = Path(__file__).parent

app = FastAPI(title="Lux Democracy Tracker", version="0.1.0")

# static / templates
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Jinja helpers
templates.env.globals["now"] = lambda: datetime.now().year  # {{ now() }}

def fmt_date(dt) -> str:
    if not dt:
        return "TBD"
    try:
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return str(dt)

templates.env.filters["fmt_date"] = fmt_date                # {{ date|fmt_date }}
templates.env.filters["fmt_money"] = lambda x: f"{x:,.0f}" if x else "—"  # {{ x|fmt_money }}

# --------------------------------------------------------------------
# Dependency
# --------------------------------------------------------------------
DbSession = Annotated[Session, Depends(get_session)]


# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------
def compute_status(initv: Initiative) -> str:
    """Simple status derived from dates."""
    now = datetime.now(timezone.utc)
    if initv.end_date and initv.end_date < now:
        return "Complete"
    if initv.start_date and initv.start_date > now:
        return "Planned"
    return "In delivery"


# --------------------------------------------------------------------
# Startup
# --------------------------------------------------------------------
@app.on_event("startup")
def _startup() -> None:
    # Ensure tables exist (safe if already created)
    init_metadata()


# --------------------------------------------------------------------
# Health
# --------------------------------------------------------------------
@app.get("/health", response_class=PlainTextResponse)
def health() -> str:
    return "ok"


# --------------------------------------------------------------------
# Homepage: initiatives list (filters + pagination)
# --------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def homepage(
    request: Request,
    session: DbSession,
    q: str | None = Query(None, description="Search in title/summary/body"),
    owner_id: int | None = Query(None, description="Institution/owner id"),
    date_from: str | None = Query(None, description="ISO date start filter (YYYY-MM-DD)"),
    date_to: str | None = Query(None, description="ISO date end filter (YYYY-MM-DD)"),
    sort_by: str | None = Query(None, description="start_date_desc|start_date_asc|budget_desc|budget_asc"),
    limit: int = Query(12, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    # Build base statement
    stmt = select(Initiative)

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            (Initiative.title.ilike(like))
            | (Initiative.summary.ilike(like))
            | (Initiative.body.ilike(like))
        )

    if owner_id:
        stmt = stmt.where(Initiative.owner_id == owner_id)

    # Parse dates if provided
    def parse_iso(d: str | None):
        if not d:
            return None
        try:
            return datetime.fromisoformat(d)
        except Exception:
            return None

    dt_from = parse_iso(date_from)
    dt_to_ = parse_iso(date_to)

    if dt_from:
        stmt = stmt.where((Initiative.start_date >= dt_from) | (Initiative.end_date >= dt_from))
    if dt_to_:
        stmt = stmt.where((Initiative.start_date <= dt_to_) | (Initiative.end_date <= dt_to_))

    # Sorting
    if sort_by == "start_date_asc":
        stmt = stmt.order_by(Initiative.start_date.asc().nulls_last())
    elif sort_by == "budget_desc":
        stmt = stmt.order_by(Initiative.budget.desc().nulls_last())
    elif sort_by == "budget_asc":
        stmt = stmt.order_by(Initiative.budget.asc().nulls_last())
    else:
        stmt = stmt.order_by(Initiative.start_date.desc().nulls_last())

    # COUNT(*) via subquery
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = session.exec(count_stmt).one()

    # Page
    initiatives = session.exec(stmt.offset(offset).limit(limit)).all()

    # Owners list for filter dropdown
    owners = session.exec(select(Institution).order_by(Institution.name)).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "initiatives": initiatives,
            "owners": owners,
            "total": total,
            "limit": limit,
            "offset": offset,
            "q": q or "",
            "owner_id": owner_id,
            "date_from": date_from or "",
            "date_to": date_to or "",
            "sort_by": sort_by or "",
            "current_year": datetime.now().year,
        },
    )


# --------------------------------------------------------------------
# Initiative detail (no Pol.is here)
# --------------------------------------------------------------------
@app.get("/initiative/{initiative_id}", response_class=HTMLResponse)
def initiative_detail(initiative_id: int, request: Request, session: DbSession):
    initiative = session.get(Initiative, initiative_id)
    if not initiative:
        raise HTTPException(status_code=404, detail="Initiative not found")

    milestones = session.exec(
        select(Milestone)
        .where(Milestone.initiative_id == initiative_id)
        .order_by(Milestone.due_date)
    ).all()

    attachments = session.exec(
        select(Attachment).where(Attachment.initiative_id == initiative_id)
    ).all()

    owner = session.get(Institution, initiative.owner_id) if initiative.owner_id else None

    return templates.TemplateResponse(
        "initiative_detail.html",
        {
            "request": request,
            "initiative": initiative,
            "milestones": milestones,
            "attachments": attachments,
            "owner": owner,
            "current_year": datetime.now().year,
        },
    )


# --------------------------------------------------------------------
# Tracker index (BuildCanada-style list of institutions)
# --------------------------------------------------------------------
@app.get("/tracker", response_class=HTMLResponse)
def tracker_index(request: Request, session: DbSession):
    insts = session.exec(select(Institution).order_by(Institution.name)).all()
    cards: list[tuple[Institution, int, int, dict[str, int]]] = []

    for inst in insts:
        inits = session.exec(select(Initiative).where(Initiative.owner_id == inst.id)).all()
        status_counts = {"Planned": 0, "In delivery": 0, "Complete": 0}
        budget_sum = 0
        for i in inits:
            status_counts[compute_status(i)] += 1
            budget_sum += i.budget or 0
        cards.append((inst, len(inits), budget_sum, status_counts))

    return templates.TemplateResponse(
        "tracker_index.html",
        {"request": request, "cards": cards, "current_year": datetime.now().year},
    )


# --------------------------------------------------------------------
# Institution detail (KPIs + by-thematic listing)
# --------------------------------------------------------------------
@app.get("/institution/{institution_id}", response_class=HTMLResponse)
def institution_detail(institution_id: int, request: Request, session: DbSession):
    inst = session.get(Institution, institution_id)
    if not inst:
        raise HTTPException(404, "Institution not found")

    base_stmt = select(Initiative).where(Initiative.owner_id == institution_id)

    # KPIs
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = session.exec(count_stmt).one()

    initiatives = session.exec(base_stmt.order_by(Initiative.start_date.desc().nulls_last())).all()

    budget_total = sum((i.budget or 0) for i in initiatives)
    buckets = {"Planned": 0, "In delivery": 0, "Complete": 0}
    for i in initiatives:
        buckets[compute_status(i)] += 1

    # Group by thematic
    thematic_map: dict[str, list[Initiative]] = {}
    for i in initiatives:
        for t in i.thematics:  # Relationship on Initiative
            thematic_map.setdefault(t.name, []).append(i)

    thematics = session.exec(select(Thematic).order_by(Thematic.name)).all()

    return templates.TemplateResponse(
        "institution_detail.html",
        {
            "request": request,
            "institution": inst,
            "initiatives": initiatives,
            "total": total,
            "budget_total": budget_total,
            "buckets": buckets,
            "thematics": thematics,
            "thematic_map": thematic_map,
            "current_year": datetime.now().year,
        },
    )


# --------------------------------------------------------------------
# Thematics: index & detail (Pol.is lives here)
# --------------------------------------------------------------------
@app.get("/thematics", response_class=HTMLResponse)
def thematics_index(request: Request, session: DbSession):
    rows = session.exec(select(Thematic).order_by(Thematic.name)).all()
    return templates.TemplateResponse(
        "thematics.html",
        {"request": request, "thematics": rows, "current_year": datetime.now().year},
    )


@app.get("/thematic/{slug}", response_class=HTMLResponse)
def thematic_detail(slug: str, request: Request, session: DbSession):
    t = session.exec(select(Thematic).where(Thematic.slug == slug)).first()
    if not t:
        raise HTTPException(404, "Thematic not found")

    initiatives = sorted(
        t.initiatives, key=lambda i: (i.start_date or datetime.min), reverse=True
    )

    # Pol.is discussions attached to this thematic
    threads = session.exec(select(Polis).where(Polis.thematic_id == t.id)).all()

    budget_total = sum((i.budget or 0) for i in initiatives)
    buckets = {"Planned": 0, "In delivery": 0, "Complete": 0}
    for i in initiatives:
        buckets[compute_status(i)] += 1

    return templates.TemplateResponse(
        "thematic_detail.html",
        {
            "request": request,
            "thematic": t,
            "initiatives": initiatives,
            "threads": threads,
            "budget_total": budget_total,
            "buckets": buckets,
            "current_year": datetime.now().year,
        },
    )

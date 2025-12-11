from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from db_model.db import get_session, init_metadata

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




def _startup() -> None:
    # Ensure tables exist (safe if already created)
    init_metadata()



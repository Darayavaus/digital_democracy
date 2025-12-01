from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional

from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

from db_model.law_commitment_link import DraftLawCommitmentLink

if TYPE_CHECKING:
    from db_model.commitment import Commitment


# ---------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------

class LawType(str, Enum):
    ProjetDeLoi = "ProjetDeLoi"
    PropositionDeLoi = "PropositionDeLoi"



class LawStatus(str, Enum):
    AviseParConferencePreside = "Avise Par Conference Presidé"
    Created = "Created"
    EnAttenteDispenseSecond = "En Attente Dispense Second"
    EnCommission = "En Commission"
    EvacueConjointement = "Evacue Conjointement"
    Fusionne = "Fusionne"
    Publie = "Publie"
    Retire = "Retired"
    Vide = "Empty"
    VoteAccepte = "Vote Accepted"
    VoteRefuse = "Vote Refused"


INPUT_LAW_STATUS_MAPPING = {
    "Cree": LawStatus.Created,
    "En Attente Dispense Second": LawStatus.EnAttenteDispenseSecond,
    "En Commission": LawStatus.EnCommission,
    "Evacue Conjointement": LawStatus.EvacueConjointement,
    "Fusionne": LawStatus.Fusionne,
    "Publie": LawStatus.Publie,
    "Retired": LawStatus.Retire,
    "Empty": LawStatus.Vide,
    'Rafu': LawStatus.Retired,
    'Refu': LawStatus.VoteRefuse,
    'Acce': LawStatus.VoteAccepte,
}


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------

class DraftLaw(SQLModel, table=True):
    __tablename__ = "draft_law"

    id: Optional[int] = Field(default=None, primary_key=True)

    law_number: int
    law_type: LawType

    law_deposit_date: Optional[date]
    law_evacuation_date: Optional[date]

    law_status: LawStatus

    law_title: str
    law_content: str
    law_authors: Optional[str]

    # Relationship (adjust back_populates according to your Commitment model)
    commitments: list["Commitment"] = Relationship(back_populates="draft_laws", link_model=DraftLawCommitmentLink)

    # -----------------------------------------------------------------
    # Validators
    # -----------------------------------------------------------------

    @staticmethod
    def _parse_ddmmyyyy(value: Any, field_name: str) -> Optional[date]:
        if value in (None, ""):
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip(), "%d/%m/%Y").date()
            except ValueError:
                raise ValueError(f"{field_name} must be in dd/mm/yyyy format")
        raise ValueError(f"Invalid type for {field_name}: {value!r}")

    @field_validator("law_deposit_date", "law_evacuation_date", mode="before")
    def _validate_dates(cls, v, info):
        return cls._parse_ddmmyyyy(v, info.field_name)

    @field_validator("law_type", mode="before")
    def _validate_type(cls, v):
        if not v:
            return None
        text = str(v).strip().lower()
        # if "projet" in text:
        #     return LawType.ProjetDeLoi
        # if "proposition" in text:
        #     return LawType.PropositionDeLoi
        return LawType(v)

    @field_validator("law_status", mode="before")
    def _validate_status(cls, v):
        if not v:
            return None
        text = str(v).strip().lower()

        if "avise" in text or "conference" in text:
            return LawStatus.AviseParConferencePreside
        if "cree" in text:
            return LawStatus.Cree
        if "attente" in text or "dispens" in text:
            return LawStatus.EnAttenteDispenseSecond
        if "commission" in text:
            return LawStatus.EnCommission
        if "evac" in text or "conjoint" in text:
            return LawStatus.EvacueConjointement
        if "fusion" in text:
            return LawStatus.Fusionne
        if "publie" in text or "publi" in text:
            return LawStatus.Publie
        if "retir" in text:
            return LawStatus.Retire
        if "vide" == text or "vide" in text:
            return LawStatus.Vide
        if "vote" in text and ("accepte" in text or "accept" in text):
            return LawStatus.VoteAccepte
        if "vote" in text and ("refus" in text or "refuse" in text):
            return LawStatus.VoteRefuse

        return LawStatus(v)

    # -----------------------------------------------------------------
    # from_row (Excel → DraftLaw)
    # -----------------------------------------------------------------

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "DraftLaw":
        """Create a DraftLaw from an Excel row with predictable column names."""

        # law_number: keep only digits
        raw_num = row.get("law_number")
        law_number = None
        if raw_num not in (None, ""):
            import re
            digits = re.sub(r"\D", "", str(raw_num))
            law_number = int(digits) if digits else None

        return cls(
            law_number=law_number,
            law_type=row.get("law_type"),
            law_deposit_date=row.get("law_deposit_date"),
            law_evacuation_date=row.get("law_evacuation_date"),
            law_status=row.get("law_status"),
            law_title=(row.get("law_title") or "").strip(),
            law_content=(row.get("law_content") or "").strip(),
            law_authors=(row.get("law_authors") or None),
        )

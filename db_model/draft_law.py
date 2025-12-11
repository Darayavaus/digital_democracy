from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional, List 

from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship

from db_model.law_commitment_link import DraftLawCommitmentLink

if TYPE_CHECKING:
    from db_model.commitment import Commitment


# ---------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------

class LawType(str, Enum):
    ProjetDeLoi = "Projet de loi"
    PropositionDeLoi = "Proposition de loi"



class LawStatus(str, Enum):
    Vide = "Vide"
    Cree = "Créé" 
    Retire = "Retiré"
    EnCommission = "En Commission"
    # Les travaux en commission se terminent par l’adoption d’un rapport. 
    # Ce dernier contient le texte final du projet ou de la proposition tel 
    # qu’il est présenté et discuté en séance publique.
    EvacueConjointement = "Evacuation conjointe"
    Fusionne = "Fusionné"
    AviseParConferencePreside = "Avisé par Conférence des Présidents"
    # Sur décision de la Conférence des Présidents, 
    # le projet ou la proposition de loi est mis(e) à l’ordre du jour d’une séance publique.
    EnAttenteDispenseSecond = "En attente d'être dispensé du second vote" 
    # En principe, un second vote doit avoir lieu au moins trois mois après le premier, 
    # mais la Chambre demande généralement au Conseil d’État à être dispensée de ce second vote
    VoteAccepte = "Accepté"
    VoteRefuse = "Refusé"
    Publie = "Publié"
    # Quatre jours après sa publication au Journal officiel du Grand-Duché de Luxembourg, 
    # la loi entre en vigueur et devient obligatoire 


# Creating a dictionary matching imported strings 
# to desired Enum values (e.g. "Cree" → LawStatus.Cree = "Créé")

INPUT_LAW_STATUS_MAPPING = {
    "Cree": LawStatus.Cree,
    "EnAttenteDispenseSecond": LawStatus.EnAttenteDispenseSecond,
    "EnCommission": LawStatus.EnCommission,
    "EvacueConjointement": LawStatus.EvacueConjointement,
    "Fusionne": LawStatus.Fusionne,
    "Publie": LawStatus.Publie,
    "Retire": LawStatus.Retire,
    "Vide": LawStatus.Vide,
    "VoteAccepte": LawStatus.VoteAccepte,
    "VoteRefuse": LawStatus.VoteRefuse,
}

# ---------------------------------------------------------------------
# Declare SQLModel Class DraftLaw
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
    # commitments: list["Commitment"] = Relationship(back_populates="draft_laws", link_model=DraftLawCommitmentLink)
    commitments: List["Commitment"] = Relationship(back_populates="draft_laws", link_model=DraftLawCommitmentLink)

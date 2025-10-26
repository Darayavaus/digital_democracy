# seed_db.py
from datetime import datetime, timedelta, timezone

from sqlmodel import Session
from db import init_metadata, engine
from models.attachment import Attachment
from models.executive_level import PoliticalLevel
from models.initiative import Initiative
from models.institution import Institution
from models.milestone import Milestone
from models.polis import Polis
from models.politician import Politician


def seed() -> None:
    # Ensure tables exist
    init_metadata()

    # Open a real context-managed Session for scripts/CLI
    with Session(engine) as session:
        # Institutions
        city = Institution(name="Ville de Luxembourg", institution="Municipality", party="DP")
        ministry_env = Institution(name="Ministère de l'Environnement", institution="Ministry", party="CSV")
        session.add_all([city, ministry_env])
        session.flush()

        # Politicians
        p1 = Politician(name="Lydie Polfer", ministry="Mayor of Luxembourg City", party="DP")
        p2 = Politician(name="Patrick Goldschmidt", ministry="Alderman for Mobility", party="DP")
        p3 = Politician(name="Claude Meisch", ministry="Minister of Education", party="DP")
        session.add_all([p1, p2, p3])

        now = datetime.now(timezone.utc)

        # Initiatives
        i1 = Initiative(
            title="Tram Network Extension",
            summary="Extend the tram line to new districts to reduce congestion.",
            body="Longer description, background, stakeholders, KPIs, funding, etc.",
            start_date=now - timedelta(days=120),
            end_date=now + timedelta(days=480),
            budget=120_000_000,
            owner_id=city.id,
        )
        i2 = Initiative(
            title="Green Roofs Program",
            summary="Subsidies for green roofs on public buildings for urban cooling.",
            body="Program details, eligibility, monitoring indicators.",
            start_date=now - timedelta(days=30),
            end_date=now + timedelta(days=335),
            budget=12_500_000,
            owner_id=ministry_env.id,
        )
        session.add_all([i1, i2])
        session.flush()

        # Milestones
        m1 = Milestone(
            title="Feasibility Study",
            summary="Finalize multi-criteria analysis and align with mobility plan.",
            body="Scope, constraints, and first stakeholder workshop.",
            due_date=now - timedelta(days=60),
            budget=500_000,
            notes="On time",
            initiative_id=i1.id,
        )
        m2 = Milestone(
            title="Tender Publication",
            summary="Publish construction tender in the EU journal.",
            body="Lots A/B/C; includes track, power, signaling.",
            due_date=now + timedelta(days=45),
            budget=1_200_000,
            notes="Draft in review",
            initiative_id=i1.id,
        )
        m3 = Milestone(
            title="Pilot Roof Installations",
            summary="Complete pilots on 5 buildings to validate specs.",
            body="Monitoring sensors & maintenance SOPs included.",
            due_date=now + timedelta(days=90),
            budget=1_000_000,
            notes="Risk: contractor capacity",
            initiative_id=i2.id,
        )
        session.add_all([m1, m2, m3])

        # Attachments
        a1 = Attachment(
            title="Feasibility Report (PDF)",
            file_url="https://example.org/files/tram-feasibility.pdf",
            initiative_id=i1.id,
        )
        a2 = Attachment(
            title="Green Roofs Guidelines",
            file_url="https://example.org/files/green-roofs-guidelines.pdf",
            initiative_id=i2.id,
        )
        session.add_all([a1, a2])

        # Polis
        pol1 = Polis(
            summary="Public consultation on tram extension routing.",
            polis_url="https://pol.is/example-tram",
            initiative_id=i1.id,
        )
        pol2 = Polis(
            summary="Ideas for green roofs maintenance partnerships.",
            polis_url="https://pol.is/example-green-roofs",
            initiative_id=i2.id,
        )
        session.add_all([pol1, pol2])

        session.commit()

    print("🌱 Seed complete.")
    

if __name__ == "__main__":
    seed()
# End of seed_db.py
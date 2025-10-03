from db import get_session
from models.politician import Politician


def seed():
    with get_session() as session:
        # Insert sample politicians
        p1 = Politician(name="Lydie Polfer", ministry="Mayor of Luxembourg City", party="DP")
        p2 = Politician(name="Patrick Goldschmidt", ministry="Alderman for Mobility", party="DP")
        p3 = Politician(name="Claude Meisch", ministry="Minister of Education", party="DP")

        session.add_all([p1, p2, p3])
        session.commit()

    print("🌱 Database seeded with sample politicians ✅")


if __name__ == "__main__":
    seed()

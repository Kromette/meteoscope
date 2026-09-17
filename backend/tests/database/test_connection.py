from sqlalchemy import text

from meteoscope.database.connection import SessionLocal


def test_database_connection() -> None:
    with SessionLocal() as session:
        result = session.execute(text("SELECT 1"))

        assert result.scalar_one() == 1
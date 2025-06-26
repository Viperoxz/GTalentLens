# src/infrastructure/db/postgres.py
import os
import contextlib
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "POSTGRES_URI",
    "postgresql://hradmin:hrpass@postgres/hr_db"
)

@contextlib.contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def save_raw_text(cv_id: str, file_path: str, raw_text: str) -> None:
    """Write (or update) raw_text into cv_texts."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO cv_texts (cv_id, file_path, raw_text, status)
            VALUES (%s, %s, %s, 'text_extracted')
            ON CONFLICT (cv_id)
            DO UPDATE SET
                raw_text  = EXCLUDED.raw_text,
                status    = 'text_extracted',
                updated_at = NOW();
            """,
            (cv_id, file_path, raw_text)
        )




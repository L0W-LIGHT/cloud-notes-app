from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

# =========================
# DATABASE CONFIG
# =========================

DB_USER = "postgres"
DB_PASSWORD = "YOUR_DB_PASSWORD"
DB_HOST = "YOUR_RDS_ENDPOINT"
DB_NAME = "appdb"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(DATABASE_URL)

# =========================
# CREATE TABLE IF NOT EXISTS
# =========================

with engine.connect() as connection:

    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT
        )
    """))

    connection.commit()

# =========================
# ROUTES
# =========================

@app.get("/")
def home():

    return {
        "message": "Notes API working 🚀"
    }


@app.get("/add-note")
def add_note():

    with engine.connect() as connection:

        connection.execute(
            text(
                "INSERT INTO notes (content) VALUES ('learn docker')"
            )
        )

        connection.commit()

    return {
        "message": "Note added successfully"
    }


@app.get("/notes")
def get_notes():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT * FROM notes")
        )

        notes = result.fetchall()

    return {
        "notes": [dict(row._mapping) for row in notes]
    }


@app.get("/test-db")
def test_db():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT NOW();")
        )

        time = result.fetchone()

    return {
        "database_time": str(time[0])
    }
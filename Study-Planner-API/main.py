import os
from typing import Any

import psycopg
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from psycopg.rows import dict_row

app = FastAPI(title="Study Planner API")


class StudySessionCreate(BaseModel):
    student_id: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
    subject: str = Field(min_length=1, max_length=80)
    goal: str = Field(min_length=1, max_length=200)


def connect_database() -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=os.getenv("PGHOST", "db"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "studyplanner"),
        user=os.getenv("PGUSER", "studyplanner"),
        password=os.getenv("PGPASSWORD", ""),
        connect_timeout=3,
        row_factory=dict_row,
    )


@app.get("/")
def home() -> dict[str, str]:
    return {
        "project": "Study Planner API",
        "message": os.getenv("APP_MESSAGE", "Plan a focused study session"),
    }


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with connect_database() as connection:
            connection.execute("SELECT 1")
    except psycopg.OperationalError as error:
        raise HTTPException(status_code=503, detail="database unavailable") from error
    return {"status": "ok", "database": "connected", "framework": "fastapi"}


@app.get("/today")
def today() -> dict[str, object]:
    return {
        "tasks": [
            {"subject": "Networking", "task": "Review subnetting", "minutes": 25},
            {"subject": "Programming", "task": "Practice functions", "minutes": 30},
            {"subject": "Databases", "task": "Revise SQL joins", "minutes": 20},
        ]
    }


@app.get("/sessions")
def list_sessions() -> list[dict[str, Any]]:
    try:
        with connect_database() as connection:
            rows = connection.execute(
                """
                SELECT id, student_id, subject, goal, created_at
                FROM study_sessions
                ORDER BY id
                LIMIT 1000
                """
            ).fetchall()
    except psycopg.OperationalError as error:
        raise HTTPException(status_code=503, detail="database unavailable") from error
    return rows


@app.post("/sessions", status_code=201)
def create_session(session: StudySessionCreate) -> dict[str, Any]:
    try:
        with connect_database() as connection:
            row = connection.execute(
                """
                INSERT INTO study_sessions (student_id, subject, goal)
                VALUES (%s, %s, %s)
                RETURNING id, student_id, subject, goal, created_at
                """,
                (session.student_id, session.subject, session.goal),
            ).fetchone()
    except psycopg.OperationalError as error:
        raise HTTPException(status_code=503, detail="database unavailable") from error
    return row


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

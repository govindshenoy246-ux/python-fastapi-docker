import os

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Read environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Build database URL dynamically
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Database engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Base class
Base = declarative_base()


# Task table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


# Create task API
@app.post("/tasks")
def create_task(task: dict):

    db = SessionLocal()

    new_task = Task(title=task["title"])

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "id": new_task.id,
        "title": new_task.title
    }


# Get all tasks API
@app.get("/tasks")
def get_tasks():

    db = SessionLocal()

    tasks = db.query(Task).all()

    return [
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ]

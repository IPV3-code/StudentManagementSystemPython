from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.student import Student
from app.controllers.student_controller import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="Student CRUD API using FastAPI and SQLAlchemy",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)


@app.get("/")
def home():
    return {"message": "Student Management System API is running"}

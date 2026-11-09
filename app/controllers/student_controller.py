from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.student_service import StudentService
from app.schemas.student import (
    StudentRequest,
    StudentPatchRequest,
    StudentResponse
)

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(db: Session = Depends(get_db)):
    return StudentService(db)


@router.get("/", response_model=list[StudentResponse])
def get_all_students(service: StudentService = Depends(get_student_service)):
    return service.get_all_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_by_id(student_id: int, service: StudentService = Depends(get_student_service)):
    return service.get_student_by_id(student_id)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentRequest, service: StudentService = Depends(get_student_service)):
    return service.create_student(student_data)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentRequest, service: StudentService = Depends(get_student_service)):
    return service.update_student(student_id, student_data)


@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, patch_data: StudentPatchRequest, service: StudentService = Depends(get_student_service)):
    return service.patch_student(student_id, patch_data)


@router.delete("/{student_id}")
def delete_student(student_id: int, service: StudentService = Depends(get_student_service)):
    return service.delete_student(student_id)

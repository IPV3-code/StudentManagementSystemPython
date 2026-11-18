from fastapi import APIRouter, Depends, status, Path, Query
from httpx import Client
from app.database import get_marklogic_client

from app.services.student_service import StudentService
from app.schemas.student import (
    StudentRequest,
    StudentPatchRequest,
    StudentResponse,
    ErrorResponse,
    StudentDeleteResponse
)
from app.notifications.notiication_service import EmailNotificationService

router = APIRouter(prefix="/students", tags=["students"])


def get_student_service(
    client: Client = Depends(get_marklogic_client)
):
    notification_service = EmailNotificationService()

    return StudentService(
        client,
        notification_service
    )


@router.get("/", response_model=list[StudentResponse], summary="Get All Students", description="retrieve all students from database or filter by course")
def get_all_students(course: str = Query(default=None, description="Filter student by course", examples=["MCA"]), limit: int = Query(default=10, ge=1, le=100, description="maximum number of students to return"), offset: int = Query(default=0, ge=0, description="Number of students to skip"), service: StudentService = Depends(get_student_service)):
    return service.get_all_students(course=course, limit=limit, offset=offset)


@router.get("/{student_id}", response_model=StudentResponse, summary="Get Student By ID", description="retrieve student by ID from database", responses={404: {"model": ErrorResponse, "description": "Student not found", "content": {"application/json": {"example": {"detail": "Student not found"}}}}})
def get_student_by_id(student_id: int = Path(..., description="unique identifier of the student", gt=0, examples=[1]), service: StudentService = Depends(get_student_service)):
    return service.get_student_by_id(student_id)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, summary="create a student", description="creating new student", responses={409: {"model": ErrorResponse, "description": "Student with this email id already exists."}})
def create_student(student_data: StudentRequest, service: StudentService = Depends(get_student_service)):
    return service.create_student(student_data)


@router.put("/{student_id}", response_model=StudentResponse, summary="update student by ID", description="updating existing student using ID", responses={404: {"model": ErrorResponse, "description": "Student not found", "content": {"application/json": {"example": {"detail": "Student not found"}}}}})
def update_student(student_id: int, student_data: StudentRequest, service: StudentService = Depends(get_student_service)):
    return service.update_student(student_id, student_data)


@router.patch("/{student_id}", response_model=StudentResponse, summary="update details of existing student", description="update specific details of student using ID", responses={404: {"model": ErrorResponse, "description": "Student not found", "content": {"application/json": {"example": {"detail": "Student not found"}}}}})
def patch_student(student_id: int, patch_data: StudentPatchRequest, service: StudentService = Depends(get_student_service)):
    return service.patch_student(student_id, patch_data)


@router.delete("/{student_id}", response_model=StudentDeleteResponse, summary="delete existing student", description="delete existing student using ID", responses={404: {"model": ErrorResponse, "description": "Student not found", "content": {"application/json": {"example": {"detail": "Student not found"}}}}})
def delete_student(student_id: int, service: StudentService = Depends(get_student_service)):
    return service.delete_student(student_id)


from httpx import Client
from fastapi import HTTPException, status

from app.notifications.notiication_service import NotificationService
from app.repositories.student_repository import StudentRepository
from app.schemas.student import (
    StudentRequest,
    StudentPatchRequest,
    StudentResponse
)


class StudentService:

    def __init__(
        self,
        client: Client,
        notification_service: NotificationService
    ):
        self.repository = StudentRepository(client)
        self.notification_service = notification_service

    def get_all_students(
        self,
        course: str | None = None,
        limit: int = 10,
        offset: int = 0
    ):
        students = self.repository.get_all(course, limit, offset)

        return [
            StudentResponse.model_validate(student)
            for student in students
        ]

    def get_student_by_id(self, student_id: int):
        student = self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student Not found"
            )

        return StudentResponse.model_validate(student)

    def create_student(self, student_data: StudentRequest):
        existing_student = self.repository.get_by_email(
            student_data.email
        )

        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student with this email id already exists."
            )

        student = self.repository.create(student_data)

        self.notification_service.send_notification(
            f"New student created: {student['name']}"
        )

        return StudentResponse.model_validate(student)

    def update_student(
        self,
        student_id: int,
        student_data: StudentRequest
    ):
        updated_student = self.repository.update(
            student_id,
            student_data
        )

        if updated_student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return StudentResponse.model_validate(updated_student)

    def patch_student(
        self,
        student_id: int,
        patch_data: StudentPatchRequest
    ):
        update_data = patch_data.model_dump(exclude_unset=True)

        updated_student = self.repository.patch(
            student_id,
            update_data
        )

        if updated_student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return StudentResponse.model_validate(updated_student)

    def delete_student(self, student_id: int):
        deleted = self.repository.delete(student_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return {"message": "Student deleted successfully"}

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.student_repository import StudentRepository
from app.schemas.student import (
    StudentRequest,
    StudentPatchRequest,
    StudentResponse
)


class StudentService:
    def __init__(self, db: Session):
        self.repository = StudentRepository(db)

    def get_all_students(self):
        students = self.repository.get_all()

        return [
            StudentResponse.model_validate(student) for student in students
        ]

    def get_student_by_id(self, student_id: int):
        student = self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found")

        return StudentResponse.model_validate(student)

    def create_student(self, student_data: StudentRequest):
        student = self.repository.create(student_data)
        return StudentResponse.model_validate(student)

    def update_student(self, student_id: int, student_data: StudentRequest):
        student = self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        updated_student = self.repository.update(student, student_data)

        return (StudentResponse.model_validate(updated_student))

    def patch_student(self, student_id: int, patch_data: StudentPatchRequest):
        student = self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        update_student = patch_data.model_dump(exclude_unset=True)

        updated_student = self.repository.patch(student, update_student)

        return (StudentResponse.model_validate(updated_student))

    def delete_student(self, student_id: int):
        student = self.repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        self.repository.delete(student)

        return {"message": "Student deleted successfully"}

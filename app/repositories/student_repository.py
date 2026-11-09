from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentRequest


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Student).all()

    def get_by_id(self, student_id: int):
        return (self.db.query(Student).filter(Student.id == student_id).first())

    def create(self, student_data: StudentRequest):
        student = Student(
            name=student_data.name,
            email=student_data.email,
            age=student_data.age,
            course=student_data.course
        )

        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)

        return student

    def update(self, student: Student, student_data: StudentRequest):
        student.name = student_data.name
        student.email = student_data.email
        student.age = student_data.age
        student.course = student_data.course

        self.db.commit()
        self.db.refresh(student)

        return student

    def patch(self, student: Student, update_data: dict):
        for key, value in update_data.items():
            setattr(student, key, value)

        self.db.commit()
        self.db.refresh(student)

        return student

    def delete(self, student: Student):
        self.db.delete(student)
        self.db.commit()

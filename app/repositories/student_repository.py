
from httpx import Client, HTTPStatusError

from app.schemas.student import StudentRequest


class StudentRepository:
    def __init__(self, client: Client):
        self.client = client

    def get_by_id(self, student_id: int):
        uri = f"/students/{student_id}.json"

        response = self.client.get(
            "/v1/documents",
            params={"uri": uri}
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()

    def get_by_email(self, email: str):
        response = self.client.get(
            "/v1/search",
            params={
                "q": email,
                "format": "json"
            }
        )

        response.raise_for_status()
        results = response.json().get("results", [])

        for result in results:
            uri = result.get("uri", "")

            if uri.startswith("/students/"):
                document = self.client.get(
                    "/v1/documents",
                    params={"uri": uri}
                )
                document.raise_for_status()
                student = document.json()

                if student.get("email") == email:
                    return student

        return None

    def get_all(self, course: str | None = None, limit: int = 10, offset: int = 0):
        response = self.client.get(
            "/v1/search",
            params={
                "format": "json",
                "start": offset + 1,
                "pageLength": limit
            }
        )

        response.raise_for_status()

        results = response.json().get("results", [])
        students = []

        for result in results:
            uri = result.get("uri", "")

            if not uri.startswith("/students/"):
                continue

            document_response = self.client.get(
                "/v1/documents",
                params={"uri": uri}
            )
            document_response.raise_for_status()

            student = document_response.json()

            if course is None or student.get("course") == course:
                students.append(student)

        return sorted(students, key=lambda student: student["id"])

    def create(self, student_data: StudentRequest):
        # Get existing students to determine the next ID
        students = self.get_all(limit=10000, offset=0)

        next_id = max(
            (student["id"] for student in students),
            default=0
        ) + 1

        # Convert the Pydantic request into a dictionary
        student = student_data.model_dump()
        student["id"] = next_id

        # Store the JSON document at a known URI
        uri = f"/students/{next_id}.json"

        response = self.client.put(
            "/v1/documents",
            params={"uri": uri},
            json=student
        )

        response.raise_for_status()

        return student

    def update(self, student_id: int, student_data: StudentRequest):
        uri = f"/students/{student_id}.json"

        # Check whether the student exists
        existing_student = self.get_by_id(student_id)

        if existing_student is None:
            return None

        # Prepare the complete updated document
        updated_student = student_data.model_dump()
        updated_student["id"] = student_id

        response = self.client.put(
            "/v1/documents",
            params={"uri": uri},
            json=updated_student
        )

        response.raise_for_status()

        return updated_student

    def patch(self, student_id: int, update_data: dict):
        # Retrieve the existing student
        student = self.get_by_id(student_id)

        if student is None:
            return None

        # Apply only the fields supplied in the PATCH request
        student.update(update_data)

        uri = f"/students/{student_id}.json"

        # Save the updated document
        response = self.client.put(
            "/v1/documents",
            params={"uri": uri},
            json=student
        )

        response.raise_for_status()

        return student

    def delete(self, student_id: int):
        # Check whether the student exists
        student = self.get_by_id(student_id)

        if student is None:
            return False

        uri = f"/students/{student_id}.json"

        response = self.client.delete(
            "/v1/documents",
            params={"uri": uri}
        )

        response.raise_for_status()

        return True

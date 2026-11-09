from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.services.student_service import StudentService
from app.schemas.student import (
    StudentRequest,
    StudentPatchRequest,
)
from app.models.student import Student


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def service(mock_db):
    return StudentService(mock_db)


@pytest.fixture
def sample_student():
    return Student(
        id=1,
        name="Rahul",
        email="rahul@example.com",
        age=25,
        course="MCA"
    )


def test_get_all_students(service, sample_student):
    service.repository.get_all = MagicMock(return_value=[sample_student])
    result = service.get_all_students()

    assert len(result) == 1
    assert result[0].name == "Rahul"


def test_get_student_by_id(service, sample_student):
    service.repository.get_by_id = MagicMock(return_value=sample_student)
    result = service.get_student_by_id(1)

    assert result.id == 1
    assert result.name == "Rahul"


def test_get_student_by_id_not_found(service):
    service.repository.get_by_id = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as exception:
        service.get_student_by_id(999)

    assert exception.value.status_code == 404


def test_create_student(service, sample_student):
    request = StudentRequest(
        name="Rahul",
        email="rahul@example.com",
        age=25,
        course="MCA"
    )

    service.repository.create = MagicMock(return_value=sample_student)
    result = service.create_student(request)

    assert result.name == "Rahul"
    service.repository.create.assert_called_once_with(request)


def test_update_student(service, sample_student):
    request = StudentRequest(
        name="Rahul",
        email="rahul@example.com",
        age=26,
        course="MCA"
    )

    service.repository.get_by_id = MagicMock(return_value=sample_student)
    service.repository.update = MagicMock(return_value=sample_student)

    result = service.update_student(1, request)

    assert result.id == 1
    service.repository.update.assert_called_once_with(sample_student, request)


def test_patch_student(service, sample_student):
    patch_request = StudentPatchRequest(age=26)

    service.repository.get_by_id = MagicMock(return_value=sample_student)
    service.repository.patch = MagicMock(return_value=sample_student)

    result = service.patch_student(1, patch_request)

    assert result.id == 1
    service.repository.patch.assert_called_once_with(
        sample_student, {"age": 26})


def test_delete_student(service, sample_student):
    service.repository.get_by_id = MagicMock(return_value=sample_student)
    service.repository.delete = MagicMock()

    result = service.delete_student(1)

    assert result == {"message": "Student deleted successfully"}
    service.repository.delete.assert_called_once_with(sample_student)


def test_delete_student_not_found(service):
    service.repository.get_by_id = MagicMock(return_value=None)

    with pytest.raises(HTTPException) as exception:
        service.delete_student(999)

    assert exception.value.status_code == 404

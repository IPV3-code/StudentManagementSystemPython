
from pydantic import BaseModel, EmailStr, ConfigDict


class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str

    model_config = ConfigDict(from_attributes=True)
